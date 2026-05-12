from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import GameDocs
from pocket_api.result import Result
from pocket_api.serializers import AdminGameDocsSerializer


class AdminGameDocsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            game_doc = get_object_or_404(GameDocs, pk=pk)
            serializer = AdminGameDocsSerializer(game_doc)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = GameDocs.objects.all().order_by("p_id", "id")
        serializer = AdminGameDocsSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminGameDocsSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        game_doc = serializer.save()
        return Result.created(
            data=AdminGameDocsSerializer(game_doc).data, msg="创建成功"
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        game_doc = get_object_or_404(GameDocs, pk=kwargs["pk"])
        if GameDocs.objects.filter(p_id=game_doc.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="当前文档组下还有子文档，不能删除",
            ).to_response()

        data = AdminGameDocsSerializer(game_doc).data
        game_doc.delete()
        return Result.success(data=data, msg="删除成功").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        game_doc = get_object_or_404(GameDocs, pk=kwargs["pk"])
        serializer = AdminGameDocsSerializer(
            game_doc,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        game_doc = serializer.save()
        return Result.success(
            data=AdminGameDocsSerializer(game_doc).data, msg="修改成功"
        ).to_response()
