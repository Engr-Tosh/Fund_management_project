from django.urls import path
from .views import (
    DepositAPIView,
    WithdrawalAPIView,
    BalanceAPIView,
    TotalBalanceAPIView,
    PersonalUsageAPIView,
    TransactionLogAPIView
    
)


urlpatterns = [
    path("deposit/", DepositAPIView.as_view(), name="deposit"),
    path("withdraw/", WithdrawalAPIView.as_view(), name="withdrawal"),
    path("balance/", BalanceAPIView.as_view(), name="balance"),
    path("total_balance/", TotalBalanceAPIView.as_view(), name="total-balance"),
    path("personal/", PersonalUsageAPIView.as_view(), name="personal-usage"),
    path("transactions/", TransactionLogAPIView.as_view(), name="transaction-history"),
]