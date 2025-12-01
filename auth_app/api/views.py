from django.contrib.auth.tokens import default_token_generator
from .permissions import IsOwner, CookieJWTAuthentication
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterView(APIView):
    """
    Create a new user account.

    Returns a success message upon successful registration
    or validation errors otherwise.
    """

    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save(is_active=False)
            activation_token = default_token_generator.make_token(saved_account)

            #E-Mail an User senden
            activation_url = f"{FRONTEND_URL}/activate/{saved_account.pk}/{activation_token}"
            send_activation_email(saved_account.email, activation_url)

            data = {
                "user": {
                    "id": saved_account.id,
                    "email": saved_account.email
                },
                "token": activation_token
            }

            return Response(
                data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    """
    Refreshes the user's access token using the refresh token from cookies.

    Validates the refresh token, issues a new access token,
    and updates the access cookie.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")
        serializer = self.get_serializer(data={"refresh": refresh})

        try:
            serializer.is_valid(raise_exception=True)
        except (ValidationError, TokenError):
            return Response(
                {"detail": "Refresh token invalid!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access = serializer.validated_data.get("access")

        response = Response(
            {
                "message": "Token refreshed",
                "access": access,
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=10 * 60,
        )

        return response


class PasswordResetView(APIView):
    pass


class PasswordResetConfirmView(APIView):
    pass

