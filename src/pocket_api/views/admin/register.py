from typing import Any

from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.result import Result
from pocket_api.serializers import (
    AdminRegisterSerializer,
    AdminUserSerializer,
)


class AdminRegisterView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Result.created(
            data=AdminUserSerializer(user).data, msg="注册成功"
        ).to_response()
