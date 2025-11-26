from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterView(APIView):
    pass


class ActivateAccountView(APIView):
    pass


class CookieTokenObtainPairView(TokenObtainPairView):
    pass


class LogoutView(APIView):
    pass  


class CookieTokenRefreshView(TokenRefreshView):
    pass


class PasswordResetView(APIView):
    pass


class PasswordResetConfirmView(APIView):
    pass

