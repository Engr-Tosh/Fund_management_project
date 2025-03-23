from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    TemplateView,
    View,    
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

"""Setting up the User Authentication"""
#Homepage
class HomeView(TemplateView):
    template_name = "tiwiti/homepage.html"

#User Registration (Django built login auth is used for logging users in)
class SignUpView(CreateView):
    template_name = "tiwiti/signup.html"
    success_url = ""
    form_class = UserCreationForm

#View to ensure a user is loggedout
class LogoutView(View):
    template_name = None
    def get(self, request):
        logout(request)
        return render(request, self.template_name)

#Profile Management
class ProfileView(View):
    def get(request):
        #if the user is logged in 
        #get the user
        #return and display the user information to the user