from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import PetsTag, Tag
from pocket_api.result import Result
from pocket_api.serializers import AdminTagSerializer


class AdminTagView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        queryset = Tag.objects.all().order_by("-id")
        serializer = AdminTagSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminTagSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()
        return Result.created(
            data=AdminTagSerializer(tag).data, msg="创建成功"
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs, partial=True)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        tag = get_object_or_404(Tag, pk=kwargs["pk"])
        if PetsTag.objects.filter(tag_id=tag.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="tag is referenced by pets",
            ).to_response()

        data = AdminTagSerializer(tag).data
        tag.delete()
        return Result.success(data=data, msg="deleted").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        tag = get_object_or_404(Tag, pk=kwargs["pk"])
        serializer = AdminTagSerializer(
            tag,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()
        return Result.success(
            data=AdminTagSerializer(tag).data, msg="修改成功"
        ).to_response()
