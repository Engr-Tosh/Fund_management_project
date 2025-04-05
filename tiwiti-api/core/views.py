from rest_framework import response, generics, status
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()

"""Authentication Setup"""
# User registration api
class UserRegisterView(generics.CreateAPIView):
    """
    View to enable users register to access the API
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    

# User login view to obtain token
class UserLoginView(APIView):
    """View for authenticated users to obtain api access token"""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get(user=user)
            return response.Response({"Message": "Successfully logged in", "Token": token.key}, status=status.HTTP_200_OK)
        else:
            return response.Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

# User profile view to ensure only token authenticated users view and update their profiles
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
