from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from docapi.permissions import IsAdmin

from .models import User
from .serializers import UserSerializer


class ProtectedView(APIView):
    """
    Защищённый эндпоинт для теста аутентификации.
    Работает с JWT (API) и сессиями (браузер).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_type = "JWT" if request.auth else "Сессия"

        return Response(
            {
                "message": "Доступ разрешён!",
                "user": str(request.user),
                "auth_type": auth_type,
                "is_staff": request.user.is_staff,
            }
        )


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.is_active = True
        user.save()


class UserListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
