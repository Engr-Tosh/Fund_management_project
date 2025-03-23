"""tiwiti management urls go here"""

from django.urls import path
from .views import (
    SignUpView,
    HomeView,
    LogoutView,
    ProfileView     
)
from django.contrib.auth.views import LoginView
urlpatterns=[
    path("", HomeView.as_view(), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="tiwiti/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="tiwiti/logout.html"), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
] 