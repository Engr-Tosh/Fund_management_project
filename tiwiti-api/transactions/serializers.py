"""The serializers for my auth views would go here"""
from rest_framework import serializers
from .models import (
    Deposit,
    Withdrawal,
    Balance,
    TotalBalance,
    PersonalUsage,
    TransactionLog
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

# Total Balance Serializer for the admin
class TotalBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalBalance
        fields = [
            "total_deposits",
            "total_withdrawals",
            "displayed_total_balance",
            "personal_usage",
            "admin_total_balance",
            "updated_at"
        ]

# Personal Usage Serializer
class PersonalUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalUsage
        fields = [
            "user",            
            "type",
            "amount",
            "description",
            "updated_at"
        ]

# Transaction Log Serializer
class TransactionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLog
        fields = [
            "type",
            "user",
            "amount",
            "deposit_transaction",
            "withdrawal_transaction",
            "status",
            "updated_at"
        ]