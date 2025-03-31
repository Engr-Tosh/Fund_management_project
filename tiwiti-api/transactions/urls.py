from django.urls import path
from .views import (
    DepositView,
    WithdrawalView,
    BalanceView,
    TotalBalanceView,
    PersonalUsageView,
    TransactionLogView
    
)


urlpatterns = [
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("withdraw/", WithdrawalView.as_view(), name="withdrawal"),
    path("balance/", BalanceView.as_view(), name="balance"),
    path("total_balance/", TotalBalanceView.as_view(), name="total-balance"),
    path("personal/", PersonalUsageView.as_view(), name="personal-usage"),
    path("transactions/", TransactionLogView.as_view(), name="transaction-history"),
]