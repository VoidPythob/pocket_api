from __future__ import annotations

from typing import Any

from django.db import models
from rest_framework import viewsets
from rest_framework.request import Request

from pocket_api.models import Tag
from pocket_api.result import Result
from pocket_api.serializers import PetTagPayloadSerializer


class TagsView(viewsets.ReadOnlyModelViewSet[Tag]):
    queryset = Tag.objects.all().order_by("-id")
    serializer_class = PetTagPayloadSerializer
    http_method_names = ["get", "head", "options"]

    def list(self, request: Request, *args: Any, **kwargs: Any):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Result.success(
                data={
                    "count": self.paginator.page.paginator.count,
                    "total_pages": self.paginator.page.paginator.num_pages,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "results": serializer.data,
                },
                msg="success",
            ).to_response()

        serializer = self.get_serializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="success").to_response()

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Result.success(data=serializer.data, msg="success").to_response()

    def get_queryset(self) -> models.QuerySet[Tag]:
        return self.queryset
