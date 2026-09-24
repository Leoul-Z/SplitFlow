from django.urls import path
# pyrefly: ignore [missing-import]
from .views import RegisterView, LoginView, LogoutView, MeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/",RegisterView.as_view(), name="Register"),
    path("login/",LoginView.as_view(), name="Login"),
    path("login/refresh/",TokenRefreshView.as_view(), name="Login"),
    path("me/",MeView.as_view(), name="My_Profile"),
    path("logout/",LogoutView.as_view(), name="Logout"),
]
