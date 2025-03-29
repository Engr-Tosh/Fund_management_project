"""The serializers for my auth views would go here"""
from rest_framework import serializers
from .models import (
    Deposit,
    Withdrawal,
    Balance,
)
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model() 

"""Implementing main user features serializer"""
# Deposit Serializer
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ["amount"]

# Withdrawal Serializer
class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ["amount"]

# User balance Serializer
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ["user", "amount", "updated_at"]