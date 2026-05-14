from __future__ import annotations

from typing import Any

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.models import PetEggGroup, Pets, PetsEggGroup
from pocket_api.pagination import CustomPageNumberPagination
from pocket_api.result import Result
from pocket_api.serializers import PetEggGroupPayloadSerializer, PetListItemSerializer
from .pet_payloads import build_pet_list_payload


class EggGroupsView(viewsets.ReadOnlyModelViewSet[PetEggGroup]):
    queryset = PetEggGroup.objects.all().order_by("-id")
    serializer_class = PetEggGroupPayloadSerializer
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
                msg="查询成功",
            ).to_response()

        serializer = self.get_serializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def get_queryset(self) -> models.QuerySet[PetEggGroup]:
        return self.queryset


class EggGroupPetsView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any):
        egg_group = get_object_or_404(PetEggGroup, pk=kwargs["pk"])
        pet_ids = PetsEggGroup.objects.filter(egg_group_id=egg_group.id).values_list(
            "pet_id", flat=True
        )
        queryset = Pets.objects.filter(id__in=pet_ids).order_by("-id")

        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PetListItemSerializer(build_pet_list_payload(page), many=True)
            return Result.success(
                data={
                    "egg_group": {
                        "id": egg_group.id,
                        "name": egg_group.name,
                    },
                    "count": paginator.page.paginator.count,
                    "total_pages": paginator.page.paginator.num_pages,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "results": serializer.data,
                },
                msg="查询成功",
            ).to_response()

        serializer = PetListItemSerializer(build_pet_list_payload(queryset), many=True)
        return Result.success(
            data={
                "egg_group": {
                    "id": egg_group.id,
                    "name": egg_group.name,
                },
                "results": serializer.data,
            },
            msg="查询成功",
        ).to_response()
