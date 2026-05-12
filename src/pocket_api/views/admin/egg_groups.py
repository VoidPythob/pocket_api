from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import PetEggGroup, PetsEggGroup
from pocket_api.result import Result
from pocket_api.serializers import AdminPetEggGroupSerializer

from .pagination import build_paginated_result


class AdminPetEggGroupView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            egg_group = get_object_or_404(PetEggGroup, pk=pk)
            serializer = AdminPetEggGroupSerializer(egg_group)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = PetEggGroup.objects.all().order_by("-id")
        return build_paginated_result(
            request=request,
            queryset=queryset,
            serializer_class=AdminPetEggGroupSerializer,
            msg="查询成功",
        )

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetEggGroupSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        egg_group = serializer.save()
        return Result.created(
            data=AdminPetEggGroupSerializer(egg_group).data,
            msg="创建成功",
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        egg_group = get_object_or_404(PetEggGroup, pk=kwargs["pk"])
        if PetsEggGroup.objects.filter(egg_group_id=egg_group.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该蛋组已被宠物关联，不能删除",
            ).to_response()

        data = AdminPetEggGroupSerializer(egg_group).data
        egg_group.delete()
        return Result.success(data=data, msg="删除成功").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        egg_group = get_object_or_404(PetEggGroup, pk=kwargs["pk"])
        serializer = AdminPetEggGroupSerializer(
            egg_group,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        egg_group = serializer.save()
        return Result.success(
            data=AdminPetEggGroupSerializer(egg_group).data,
            msg="修改成功",
        ).to_response()
