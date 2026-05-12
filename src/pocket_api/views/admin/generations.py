from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import PetGeneration, PetsPetGeneration
from pocket_api.result import Result
from pocket_api.serializers import AdminPetGenerationSerializer


class AdminPetGenerationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            generation = get_object_or_404(PetGeneration, pk=pk)
            serializer = AdminPetGenerationSerializer(generation)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = PetGeneration.objects.all().order_by("-id")
        serializer = AdminPetGenerationSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetGenerationSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        generation = serializer.save()
        return Result.created(
            data=AdminPetGenerationSerializer(generation).data, msg="创建成功"
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        generation = get_object_or_404(PetGeneration, pk=kwargs["pk"])
        if PetsPetGeneration.objects.filter(generation_id=generation.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该世代已被宠物关联，不能删除",
            ).to_response()

        data = AdminPetGenerationSerializer(generation).data
        generation.delete()
        return Result.success(data=data, msg="删除成功").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        generation = get_object_or_404(PetGeneration, pk=kwargs["pk"])
        serializer = AdminPetGenerationSerializer(
            generation,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        generation = serializer.save()
        return Result.success(
            data=AdminPetGenerationSerializer(generation).data, msg="修改成功"
        ).to_response()
