from django.urls import path

from .views import RegisterView
from .views import ActivationView
from .views import CookieTokenObtainPairView
from .views import LogoutView
from .views import CookieTokenRefreshView
from .views import PasswordResetView
from .views import PasswordResetConfirmView


"""
    URL routes for authentication-related API endpoints.

    Includes endpoints for:
    - User registration and email activation
    - Login with cookie-based JWT tokens
    - Logout and token invalidation
    - Refreshing access tokens via refresh cookie
    - Password reset request and confirmation
"""

app_name = 'auth_app'

urlpatterns = [
    path("register/",
         RegisterView.as_view(),
         name="register"),
    path("activate/<uidb64>/<token>/",
         ActivationView.as_view(),
         name="activation_via_email"),
    path("login/",
         CookieTokenObtainPairView.as_view(),
         name="login"),
    path("logout/",
         LogoutView.as_view(),
         name="logout"),
    path("token/refresh/",
         CookieTokenRefreshView.as_view(),
         name="token_refresh"),
    path("password_reset/",
         PasswordResetView.as_view(),
         name="password_reset"),
    path("password_confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
]
