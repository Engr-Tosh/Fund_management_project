from django.contrib import admin
from .models import CustomUser

#Registering the customuser admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username")
    list_filter = ("email", "username")
    search_fields = ("email", "username")

admin.site.register(CustomUser, CustomUserAdmin)