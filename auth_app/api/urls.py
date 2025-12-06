from django.urls import path

from .views import RegisterView, PasswordResetView, LogoutView, CookieTokenObtainPairView, CookieTokenRefreshView, PasswordResetConfirmView

"""
    URL routes for authentication-related API endpoints.

    Includes endpoints for:
    - User registration
    - Account activation via email link
    - Login with JWT tokens (stored in cookies)
    - Logout and token invalidation
    - Refreshing access tokens using refresh cookies
    - Password reset and password reset confirmation
"""
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    # path("activate/<str:uidb64>/<str:token>/", VerifyEmailView.as_view(), name="verify_email"),
    path("login/", CookieTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("token/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("token/password_confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]