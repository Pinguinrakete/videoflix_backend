from django.urls import path

from .views import RegisterView, ActivationView, CookieTokenObtainPairView, LogoutView, CookieTokenRefreshView, PasswordResetView, PasswordResetConfirmView

"""
    URL routes for authentication-related API endpoints.

    Includes endpoints for:
    - User registration and email activation
    - Login with cookie-based JWT tokens
    - Logout and token invalidation
    - Refreshing access tokens via refresh cookie
    - Password reset request and confirmation
"""
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", ActivationView.as_view(), name="activation_via_email"),
    path("login/", CookieTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("token/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("token/password_confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]