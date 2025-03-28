"""The serializers for my views would go here"""
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
User = get_user_model() 

#User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "phone", "created_at"]

# User registration serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    This serializer returns a token key after the succesful creation of a user"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data("email"),
            phone = validated_data("phone"),
            password = validated_data["password"],
        )
        token = Token.objects.create(user=user)
        return user

# User login serializer
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid Username or password")
        
        data['user'] = user
        return data

    