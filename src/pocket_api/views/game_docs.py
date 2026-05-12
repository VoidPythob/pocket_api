from __future__ import annotations

from typing import Any

from django.db import models
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.models import GameDocs
from pocket_api.result import Result
from pocket_api.serializers import (
    GameDocCategorySerializer,
    GameDocDetailSerializer,
    GameDocListItemSerializer,
    GameDocsQuerySerializer,
)


class GameDocsView(viewsets.ReadOnlyModelViewSet[GameDocs]):
    queryset = GameDocs.objects.all().order_by("-id")
    serializer_class = GameDocDetailSerializer
    http_method_names = ["get", "head", "options"]

    def list(self, request: Request, *args: Any, **kwargs: Any):
        query_serializer = GameDocsQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        group_id = query_serializer.validated_data.get("group_id")

        queryset = self.get_queryset()
        if group_id is not None:
            queryset = queryset.filter(p_id=group_id)

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self._build_list_payload(page)
            serializer = GameDocListItemSerializer(data, many=True)
            return Result.success(
                data={
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "results": serializer.data,
                },
                msg="查询成功",
            ).to_response()

        data = self._build_list_payload(queryset)
        serializer = GameDocListItemSerializer(data, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        serializer = GameDocDetailSerializer(
            {
                "id": instance.id,
                "p_id": instance.p_id,
                "name": instance.name,
                "path": instance.path,
                "content": instance.content,
            }
        )
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def get_queryset(self) -> models.QuerySet[GameDocs]:
        group_ids = GameDocs.objects.filter(
            models.Q(p_id__isnull=True) | models.Q(p_id=0)
        ).values_list("id", flat=True)
        return self.queryset.filter(p_id__in=group_ids)

    @staticmethod
    def _build_list_payload(
        game_docs: list[GameDocs] | models.QuerySet[GameDocs],
    ) -> list[dict[str, Any]]:
        return [
            {
                "id": game_doc.id,
                "p_id": game_doc.p_id,
                "name": game_doc.name,
                "path": game_doc.path,
            }
            for game_doc in game_docs
        ]


class GameDocCategoriesView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any):
        groups = list(
            GameDocs.objects.filter(models.Q(p_id__isnull=True) | models.Q(p_id=0)).order_by(
                "-id"
            )
        )
        group_ids = [group.id for group in groups]
        child_docs = list(GameDocs.objects.filter(p_id__in=group_ids).order_by("id"))

        children_map: dict[int, list[dict[str, Any]]] = {group_id: [] for group_id in group_ids}
        for child in child_docs:
            children_map.setdefault(child.p_id, []).append(
                {
                    "id": child.id,
                    "p_id": child.p_id,
                    "name": child.name,
                    "path": child.path,
                }
            )

        serializer = GameDocCategorySerializer(
            [
                {
                    "id": group.id,
                    "p_id": group.p_id,
                    "name": group.name,
                    "path": group.path,
                    "children": children_map.get(group.id, []),
                }
                for group in groups
            ],
            many=True,
        )
        return Result.success(data=serializer.data, msg="查询成功").to_response()
