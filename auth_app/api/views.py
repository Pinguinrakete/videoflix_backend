from .permissions import IsOwner, CookieJWTAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterView(APIView):
    pass


class ActivateAccountView(APIView):
    pass


class CookieTokenObtainPairView(TokenObtainPairView):
    pass


class LogoutView(APIView):
    """
    Logs out the authenticated user by blacklisting the refresh token
    and removing authentication cookies.
    """

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception as e:
            print(f"Failed to move the token to the blacklist: {e}")

        response = Response(
            {
                "detail": (
                    "Log-Out successfully! All Tokens will be deleted. "
                    "Refresh token is now invalid."
                )
            },
            status=status.HTTP_200_OK,
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CookieTokenRefreshView(TokenRefreshView):
    pass


class PasswordResetView(APIView):
    pass


class PasswordResetConfirmView(APIView):
    pass

