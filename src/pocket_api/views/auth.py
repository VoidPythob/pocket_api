from typing import Any

from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.result import Result
from pocket_api.serializers import AdminLoginSerializer, AdminUserSerializer


class AdminLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Result.from_code(
                ResponseCode.UNAUTHORIZED, msg="邮箱或密码错误"
            ).to_response()

        login(request, user)

        user.last_login_ip = self._get_client_ip(request)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login_ip", "last_login"])
        user.refresh_from_db(fields=["last_login_ip", "last_login"])

        return Result.success(
            data=AdminUserSerializer(user).data, msg="登录成功"
        ).to_response()

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")


class AdminLogoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request: Request, *args: Any, **kwargs: Any):
        user = request.user
        user.last_logout_time = timezone.now()
        user.save(update_fields=["last_logout_time"])
        logout(request)
        return Result.success(msg="退出成功").to_response()
