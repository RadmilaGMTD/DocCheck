from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig

from .views import ProtectedView, UserCreateApiView, UserListApiView

app_name = UsersConfig.name


urlpatterns = [
    path("create/", UserCreateApiView.as_view(), name="users_create"),
    path("list/", UserListApiView.as_view(), name="users_list"),
    path("token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html", next_page="/users/protected/"),
        name="login",
    ),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
