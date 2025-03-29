from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


"""The models for my fund management system"""
# Core functionality models
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    


