from __future__ import annotations

from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import PetFeature, PetsPetFeature
from pocket_api.result import Result
from pocket_api.serializers import AdminPetFeatureSerializer


class AdminPetFeatureView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            feature = get_object_or_404(PetFeature, pk=pk)
            serializer = AdminPetFeatureSerializer(feature)
            return Result.success(data=serializer.data, msg="success").to_response()

        name = request.query_params.get("name", "").strip()
        queryset = PetFeature.objects.all().order_by("-id")
        if name:
            queryset = queryset.filter(introduction__icontains=name)

        serializer = AdminPetFeatureSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="success").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetFeatureSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        feature = serializer.save()
        return Result.created(
            data=AdminPetFeatureSerializer(feature).data,
            msg="created",
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        feature = get_object_or_404(PetFeature, pk=kwargs["pk"])
        if PetsPetFeature.objects.filter(feature_id=feature.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="feature is referenced by pets",
            ).to_response()

        data = AdminPetFeatureSerializer(feature).data
        feature.delete()
        return Result.success(data=data, msg="deleted").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        feature = get_object_or_404(PetFeature, pk=kwargs["pk"])
        serializer = AdminPetFeatureSerializer(
            feature,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        feature = serializer.save()
        return Result.success(
            data=AdminPetFeatureSerializer(feature).data,
            msg="updated",
        ).to_response()
