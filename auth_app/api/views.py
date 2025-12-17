from .utils import send_activation_email, send_reset_password_email
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .permissions import IsOwner, CookieJWTAuthentication
from .serializers import RegisterSerializer, CookieTokenObtainPairSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import django_rq

User = get_user_model()


class RegisterView(APIView):
    """
    Create a new user account.

    Returns a success message upon successful registration
    or validation errors otherwise.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_token = default_token_generator.make_token(user)

            activation_url = (
                f'http://127.0.0.1:5500/pages/auth/activate.html'
                f'?uid={uid}&token={activation_token}'
            )

            django_rq.get_queue('default').enqueue(
                send_activation_email,
                user.email,
                activation_url
            )

            return Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "token": activation_token,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )


class ActivationView(APIView):
    """
    Activate a user account using a UID and token.

    Returns a success message if activation is successful,
    or an error message if the link is invalid, expired, or already used.
    """

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response(
                {"detail": "Invalid user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired activation token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.is_active:
            return Response(
                {"detail": "Account already activated."},
                status=status.HTTP_200_OK
            )

        user.is_active = True
        user.is_verified = True
        user.save()

        return Response(
            {"detail": "Account successfully activated."},
            status=status.HTTP_200_OK
        )


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Handle user login and set JWT cookies.

    On success, returns user details and sets access/refresh tokens
    as HTTP-only cookies. Returns 401 if authentication fails.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CookieTokenObtainPairSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            response = Response(
                {
                    "detail": "Login successfully!",
                    "user": {
                        "id": user.id,
                        "username": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=False,
                samesite="None",
                max_age=10 * 60,
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="None",
                max_age=24 * 60 * 60,
            )

            return response

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


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
    """
    Initiate a password reset for a user.

    Sends a password reset email if the provided data is valid,
    otherwise returns validation errors.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_token = default_token_generator.make_token(user)

            reset_pw_url = (
                f'http://127.0.0.1:5500/pages/auth/confirm_password.html'
                f'?uid={uid}&token={reset_token}'
            )

            django_rq.get_queue('default').enqueue(
                send_reset_password_email,
                user.email,
                reset_pw_url
                )

            return Response(
                {
                    "detail": "An email has been sent to reset your password."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetConfirmView(APIView):
    """
    Reset a user's password using UID and token from a reset link.
    Returns success or error messages.
    """

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid link."},
                status=status.HTTP_400_BAD_REQUEST
                )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
                )

        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Your Password has been successfully reset."},
            status=status.HTTP_200_OK
            )