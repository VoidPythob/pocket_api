from __future__ import annotations

from typing import Any

from django.db import models
from rest_framework import viewsets
from rest_framework.request import Request

from pocket_api.models import ItemCategory, Items, ItemsItemCategory
from pocket_api.result import Result
from pocket_api.serializers import ItemListQuerySerializer, ItemPayloadSerializer


class ItemsView(viewsets.ReadOnlyModelViewSet[Items]):
    queryset = Items.objects.all().order_by("-id")
    serializer_class = ItemPayloadSerializer
    http_method_names = ["get", "head", "options"]

    def list(self, request: Request, *args: Any, **kwargs: Any):
        query_serializer = ItemListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        category_id = query_serializer.validated_data.get("category_id")
        name = query_serializer.validated_data.get("name")

        queryset = self.filter_queryset(self.get_queryset())
        if category_id:
            item_ids = ItemsItemCategory.objects.filter(category_id=category_id).values_list(
                "item_id", flat=True
            )
            queryset = queryset.filter(id__in=item_ids)
        if name:
            queryset = queryset.filter(name__icontains=name)

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self._build_payload(page)
            serializer = self.get_serializer(data, many=True)
            return Result.success(
                data={
                    "count": self.paginator.page.paginator.count,
                    "total_pages": self.paginator.page.paginator.num_pages,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "results": serializer.data,
                },
                msg="查询成功",
            ).to_response()

        data = self._build_payload(queryset)
        serializer = self.get_serializer(data, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        data = self._build_payload([instance])[0]
        serializer = self.get_serializer(data)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def get_queryset(self) -> models.QuerySet[Items]:
        return self.queryset

    @staticmethod
    def _build_payload(
        items: list[Items] | models.QuerySet[Items],
    ) -> list[dict[str, Any]]:
        item_list = list(items)
        item_ids = [item.id for item in item_list]
        if not item_ids:
            return []

        relations = list(ItemsItemCategory.objects.filter(item_id__in=item_ids))
        category_ids = [relation.category_id for relation in relations]
        category_map = {
            category.id: category
            for category in ItemCategory.objects.filter(id__in=category_ids)
        }

        item_categories_map: dict[int, list[dict[str, Any]]] = {
            item_id: [] for item_id in item_ids
        }
        for relation in relations:
            category = category_map.get(relation.category_id)
            if category is None:
                continue
            item_categories_map.setdefault(relation.item_id, []).append(
                {
                    "id": category.id,
                    "name": category.name,
                }
            )

        return [
            {
                "id": item.id,
                "name": item.name,
                "jp_name": item.jp_name,
                "en_name": item.en_name,
                "introduction": item.introduction,
                "detail": item.detail,
                "categories": item_categories_map.get(item.id, []),
            }
            for item in item_list
        ]
