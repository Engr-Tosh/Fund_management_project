from django.shortcuts import render
from rest_framework import response, generics, status
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
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import authenticate

# Authenticated Users can make deposits
class DepositView(generics.ListCreateAPIView):
    """Users can make deposits"""
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

# Authenticated Users can make withdrawals
class WithdrawalView(generics.ListCreateAPIView):
    """Users can place withdrawals"""
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [permissions.IsAuthenticated]

# Authenticated Users can see their balance:
class BalanceView(generics.RetrieveAPIView):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

"""Admin-View of Balances"""
# Total Balance
class TotalBalanceView(generics.RetrieveAPIView):
    queryset = TotalBalance
    serializer_class = TotalBalanceSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

class PersonalUsageView(generics.RetrieveAPIView):
    queryset = PersonalUsage
    serializer_class = PersonalUsageSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

class TransactionLogView(generics.RetrieveAPIView):
    queryset = TransactionLog
    serializer_class = TransactionLogSerializer
    permission_classes = [permissions.IsAuthenticated]