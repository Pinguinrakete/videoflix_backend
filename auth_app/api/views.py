from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .permissions import IsOwner, CookieJWTAuthentication
from .serializers import RegisterSerializer, CookieTokenObtainPairSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import reverse


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
            user = serializer.save()

            # UID & Token erzeugen
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_token = default_token_generator.make_token(user)

            # Verifikationslink erstellen
            # verification_url = request.build_absolute_uri(
            #     reverse('verify_email', kwargs={'uidb64': uid, 'token': activation_token})
            # )

            # E-Mail senden
            try:
                send_mail(
                    subject='Verify your account',
                    message=f'Please click the link to verify your account: click mich',
                    # message=f'Please click the link to verify your account: {verification_url}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            except Exception as e:
                return Response(
                    {"error": "Email could not be sent", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Sicherheits-Response (Token NICHT zurückgeben!)
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email
                    },
                    "message": "Account created. Please check your email to verify your account."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Handle user login and set JWT cookies.

    On success, returns user details and sets access/refresh tokens
    as HTTP-only cookies. Returns 401 if authentication fails.
    """

    authentication_classes = [JWTAuthentication]
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
                        "username": user.username,
                        "email": user.email,
                    },
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

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
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
    pass


class PasswordResetConfirmView(APIView):
    pass

