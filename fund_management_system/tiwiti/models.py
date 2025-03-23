from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

"""Using a custom user model for access"""
#Create a custom user manager for the user model management
class CustomUserManager(BaseUserManager):
    """User manager:
    Which includes the methods for the creation of a user"""

    def create_user(self, email=None, username=None, password=None, **extra_fields):
        """Create and return user with usernam and password"""
        #If the email isn't provided raise an error
        if not email:
            raise ValueError("Email field is required")
        
        #if the username isn't provided raise an error
        if not username:
             raise ValueError("Please provide username")
        
        #if the password isn't provided
        if not password:
             raise ValueError("password wasn't provided")
        
        email = self.normalize_email(email)     #Converts the string into all lowercase
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        
        user.save()   #Saves information to the database
        return user

    """creating a superuser"""
    def create_superuser(self, email=None, username=None, password=None, **extra_fields):
           extra_fields.setdefault("is_staff", True)
           extra_fields.setdefault("is_superuser", True)

           return self.create_user(email=email, username=username, password=password, **extra_fields)

"""The custom user model the base user manager would work on"""
class CustomUser(AbstractUser):
     email = models.EmailField(unique=True)
     objects = CustomUserManager()
     

     USERNAME_FIELD ="username" #Users are to log in with username
     REQUIRED_FIELDS = [email]  #email is required for user creation

     def __str__(self):
          return self.username