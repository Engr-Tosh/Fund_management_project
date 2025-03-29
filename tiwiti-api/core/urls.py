from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserProfileView,
    DepositView,
    WithdrawalView,
    BalanceView
)


urlpatterns = [
    path("register/", UserRegisterView.as_view(), name='register'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("withdrawal/", WithdrawalView.as_view(), name="withdrawal"),
    path("balance/", BalanceView.as_view(), name="balance")    
]