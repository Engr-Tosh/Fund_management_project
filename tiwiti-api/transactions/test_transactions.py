from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from .models import (
    Deposit,
    Withdrawal,
    Balance,
    TransactionLog,
    TotalBalance,
    PersonalUsage
)
from decimal import Decimal

User = get_user_model()

class TransactionAPITestCase(APITestCase):

    def setUp(self):
        """
        Setup test users and intial balance
        """

        #Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")

        #Authenticate a user
        self.client.login(username="testuser", password="testpass")

        # Generate authentication tokens
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)

        # Initial balance for the user
        self.balance = Balance.objects.create(user=self.user, amount=Decimal("100.00"))


        # Define API endpoints
        self.deposit_url = reverse("deposit")
        self.withdraw_url = reverse("withdrawal")
        self.balance_url = reverse("balance")
        self.transaction_log_url = reverse("transaction-history")
        self.total_balance_url = reverse("total-balance")
        self.personal_usage_url = reverse("personal-usage")

    def authenticate_user(self):
        """Authenticate as a regular user by setting the authorization header."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_token.key}")

    def authenticate_admin(self):
        """Authenticate as an admin user by setting the authorization header."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

    def test_unauthenticated_requests_fail(self):
        """
        Ensure that unauthenticated requests are rejected with 401 Unauthorized.
        """
        response = self.client.get(self.balance_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_make_deposit(self):
        """
        Test that an authenticated user can make a deposit and that it updates their balance and transaction log.
        """
        self.authenticate_user()
        deposit_data = {"amount": "50.00"}
        response = self.client.post(self.deposit_url, deposit_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that deposit was recorded
        self.assertEqual(Deposit.objects.count(), 1)
        
        # Check that balance updated
        self.balance.refresh_from_db()
        self.assertEqual(self.balance.amount, Decimal("150.00"))

        # Check that transaction log is created
        self.assertEqual(TransactionLog.objects.count(), 1)
        self.assertEqual(TransactionLog.objects.first().type, "deposit")


    """Withdrawal Tests"""
    def test_user_can_make_withdrawal(self):
        """
        Test that an authenticated user can withdraw funds successfully and that it updates their balance and transaction log.
        """
        self.authenticate_user()
        withdrawal_data = {"amount": "30.00"}
        response = self.client.post(self.withdraw_url, withdrawal_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that withdrawal was recorded
        self.assertEqual(Withdrawal.objects.count(), 1)

        # Check that balance updated
        self.balance.refresh_from_db()
        self.assertEqual(self.balance.amount, Decimal("70.00"))

        # Check that transaction log is created
        self.assertEqual(TransactionLog.objects.count(), 1)
        self.assertEqual(TransactionLog.objects.first().type, "withdrawal")

    
    def test_user_cannot_withdraw_more_than_balance(self):
        """
        Test that an authenticated user cannot withdraw more than their available balance.
        """
        self.authenticate_user()
        withdrawal_data = {"amount": "200.00"}  # More than available balance
        response = self.client.post(self.withdraw_url, withdrawal_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure balance remains unchanged
        self.balance.refresh_from_db()
        self.assertEqual(self.balance.amount, Decimal("100.00"))

        # Ensure no transaction log was created
        self.assertEqual(TransactionLog.objects.count(), 0)


    def test_user_can_view_balance(self):
        """
        Test that an authenticated user can retrieve their current balance.
        """
        self.authenticate_user()
        response = self.client.get(self.balance_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "100.00")

    
    def test_user_can_view_transaction_log(self):
        """
        Test that an authenticated user can retrieve their own transaction history.
        """
        self.authenticate_user()

        # Creating a transaction log entry
        Deposit.objects.create(user=self.user, amount=Decimal("50.00"))

        response = self.client.get(self.transaction_log_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    
    def test_admin_can_view_total_balance(self):
        """
        Test that only an admin can access the total balance API.
        """
        self.authenticate_user()
        response = self.client.get(self.total_balance_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_cannot_view_total_balance(self):
        """
        Test that non-admin can't access the total balance API.
        """
        self.authenticate_admin()
        response = self.client.get(self.total_balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_view_personal_usage(self):
        """
        Test that only an admin can access the personal usage API.
        """
        self.authenticate_admin()
        response = self.client.get(self.personal_usage_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_view_personal_usage(self):
        """
        Test that a regular users can't access the personal usage API.
        """
        self.authenticate_user()
        response = self.client.get(self.personal_usage_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    


    # def test_personal_usage_creation_updates_total_balance(self):
    #     """
    #     Test that creating a PersonalUsage entry updates the TotalBalance.
    #     """

    #     # Authenticate as admin (assuming you already have an admin setup)
    #     self.authenticate_admin()

    #     # Create a user for testing
    #     User = get_user_model()
    #     user = User.objects.create_user(username="testuser1", password="password123")

    #     # Create and obtain a token for the newly created user
    #     token = Token.objects.create(user=user)
    #     headers = {'Authorization': f'Token {token.key}'}

    #     # Ensure the user has made a deposit
    #     deposit_data = {
    #         "user": user.id,
    #         "amount": "100.00",
    #         "type": "deposit"
    #     }
    #     response = self.client.post(self.deposit_url, deposit_data, **headers)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Now, perform the PersonalUsage deduction
    #     personal_usage_data = {
    #         "type": "deduction",
    #         "amount": "20.00",
    #         "description": "Admin deduction"
    #     }
    #     response = self.client.post(self.personal_usage_url, personal_usage_data, **headers)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Fetch the updated TotalBalance
    #     total_balance = TotalBalance.objects.first()

    #     # Check that the TotalBalance reflects the deduction and available funds
    #     self.assertEqual(total_balance.personal_usage, Decimal('20.00'))
    #     self.assertEqual(total_balance.admin_total_balance, Decimal('80.00'))  # 100 - 20 = 80
