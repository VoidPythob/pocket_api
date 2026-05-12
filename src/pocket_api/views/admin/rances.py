from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import PetRance, PetsPetRance
from pocket_api.result import Result
from pocket_api.serializers import AdminPetRanceSerializer

from .pagination import build_paginated_result


class AdminPetRanceView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            rance = self._get_active_rance(pk)
            serializer = AdminPetRanceSerializer(rance)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = PetRance.objects.filter(is_delete=0).order_by("-id")
        return build_paginated_result(
            request=request,
            queryset=queryset,
            serializer_class=AdminPetRanceSerializer,
            msg="查询成功",
        )

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetRanceSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        rance = serializer.save()
        return Result.created(
            data=AdminPetRanceSerializer(rance).data,
            msg="创建成功",
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        rance = self._get_active_rance(kwargs["pk"])
        if PetsPetRance.objects.filter(rance_id=rance.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该种族已被宠物关联，不能删除",
            ).to_response()

        rance.is_delete = 1
        rance.modified_by = request.user.id
        rance.modified_at = timezone.now()
        rance.save(update_fields=["is_delete", "modified_by", "modified_at"])
        return Result.success(
            data=AdminPetRanceSerializer(rance).data,
            msg="删除成功",
        ).to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        rance = self._get_active_rance(kwargs["pk"])
        serializer = AdminPetRanceSerializer(
            rance,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        rance = serializer.save()
        return Result.success(
            data=AdminPetRanceSerializer(rance).data,
            msg="修改成功",
        ).to_response()

    @staticmethod
    def _get_active_rance(pk: int) -> PetRance:
        return get_object_or_404(PetRance, pk=pk, is_delete=0)
