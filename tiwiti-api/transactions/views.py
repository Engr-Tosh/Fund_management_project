from django.shortcuts import render
from rest_framework import response, generics, status
from .serializers import (
    DepositSerializer,
    WithdrawalSerializer,
    BalanceSerializer,
)
from .models import (
    Deposit,
    Withdrawal,
    Balance,
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