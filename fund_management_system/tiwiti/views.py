from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    TemplateView,
    View,    
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

"""Setting up the User Authentication"""
#Homepage (Displays the homepage)
class HomeView(TemplateView):
    template_name = "tiwiti/homepage.html"


# User Registration 
# Uses Django built UserCreationForm for user signup
User = get_user_model()

class SignUpView(CreateView):
    model = User        #Specifies the user model being used (instead of auth.user)
    template_name = "tiwiti/signup.html"
    success_url = reverse_lazy("login")     # Redirects to login page after successful signup
    form_class = UserCreationForm       # Uses Django's default user creation form

    def get_form_class(self):
        """ 
        Returns a customized UserCreationForm that includes the 'email' field.
        This ensures the form is linked to the custom user model.
        """
        class CustomUserCreationForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = User        # Uses the custom user model
                fields = ("username", "email", "password1", "password2")
            
        return CustomUserCreationForm
    

# Logout View
# Handles user logout functionality
class LogoutView(View):
    template_name = None
    def get(self, request):
        logout(request)     # Logs out the user
        return render(request, self.template_name)      # Redirects to the specified template if provided


# Profile Management View
# Uses LoginRequiredMixin to ensure only logged-in users can access this view
class ProfileView(LoginRequiredMixin, View):
    template_name = "tiwiti/userprofile.html"
    
    def get(self, request):
        """Handles GET requests and displays user profile information"""
        user = request.user
        context = {"user": user}        # Passes user info to the template
        return render(request, self.template_name, context)     #Renders the profile page 

    def post(self , request):
        """Handles POST requests and updates the user's email"""
        user = request.user     # Get the currently logged-in user

        if request.method == "POST":       
            updated_email = request.POST.get("email")     # Get updated email from form input
            
            # If email is provided and different from the current email, update it
            if updated_email and updated_email != user.email:
                user.email = updated_email
                user.save()    # Save changes to the database

        return redirect("profile")  # Reirect back to the profile page

            
            