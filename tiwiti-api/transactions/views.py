from rest_framework import generics, pagination
from .serializers import (
    DepositSerializer,
    WithdrawalSerializer,
    BalanceSerializer,
    TotalBalanceSerializer,
    PersonalUsageSerializer,
    TransactionLogSerializer
)
from .models import (
    Deposit,
    Withdrawal,
    Balance,
    TotalBalance,
    PersonalUsage,
    TransactionLog 
)
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

# Authenticated Users can make deposits
class DepositAPIView(generics.ListCreateAPIView):
    """Users can make deposits"""
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    # Ensure authenticated users can only get his/her own info/make deposit to his or her account
    def get_queryset(self):
        return Deposit.objects.select_related("user").filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Authenticated Users can make withdrawals
class WithdrawalAPIView(generics.ListCreateAPIView):
    """Users can place withdrawals"""
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    # Ensure authenticated users can only get his/her own info/make withdrawal from his or her account
    def get_queryset(self):
        return Withdrawal.objects.select_related("user").filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data.get("amount")

        try:
            user_balance = Balance.objects.get(user=user)

        except Balance.DoesNotExist:
            raise ValidationError({"Message": "No Balance Record found for this user"})

        if amount > user_balance.amount:
            raise ValidationError({"Message": "Insufficient Balance"})

        serializer.save(user=user)

    

# Authenticated Users can see their balance:
class BalanceAPIView(generics.RetrieveAPIView):
    """Authenticated Users can view their balance"""
    queryset = Balance.objects.select_related("user").all()
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure authenticated users can only get his/her own info/make withdrawal from his or her account
    # Display the most recent balance(a single instance)
    def get_object(self):
        return self.queryset.get(user=self.request.user)
        

"""Admin-View of Balances"""
# Total Balance
class TotalBalanceAPIView(generics.RetrieveAPIView):
    """Admin view of the all user balance"""
    queryset = TotalBalance.objects.all()
    serializer_class = TotalBalanceSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    # Display the most recent balance(a single instance)
    def get_object(self):
        return TotalBalance.objects.order_by("-updated_at").first() or TotalBalance()

class PersonalUsageAPIView(generics.ListCreateAPIView):
    queryset = PersonalUsage.objects.order_by("-updated_at").all()
    serializer_class = PersonalUsageSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination


class TransactionLogAPIView(generics.ListAPIView):
    serializer_class = TransactionLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    # Ensure authenticated users can only get his/her own transaction info from his or her account
    def get_queryset(self):
        return TransactionLog.objects.select_related("user").prefetch_related("deposit_transaction", "withdrawal_transaction").filter(user=self.request.user)