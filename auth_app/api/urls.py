from django.urls import path

from .views import RegisterView, ActivateAccountView, LogoutView, CookieTokenObtainPairView, CookieTokenRefreshView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<str:uidb64>/<str:token>/", ActivateAccountView(), name="activate_account"),
    path("login/", CookieTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]