from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterView(APIView):
    pass


class ActivateAccountView(APIView):
    pass


class ResetPasswordView(APIView):
    pass


class ChangePasswordView(APIView):
    pass


class CookieTokenObtainPairView(TokenObtainPairView):
    pass


class CookieTokenRefreshView(TokenRefreshView):
    pass


class LogoutView(APIView):
    pass  
