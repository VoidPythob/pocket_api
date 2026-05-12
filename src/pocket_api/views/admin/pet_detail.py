from __future__ import annotations

from typing import Any

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.models import (
    PetGuide,
    PetImage,
    Pets,
    PetsAttribute,
    PetsEggGroup,
    PetsPetFeature,
    PetsPetGeneration,
    PetsPetGuide,
    PetsPetRance,
    PetsPetRegion,
    PetsPetSkill,
    PetsTag,
)
from pocket_api.result import Result
from pocket_api.serializers import AdminPetCreateSerializer, AdminPetUpdateSerializer


class AdminPetDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pk"])
        data = AdminPetCreateSerializer.build_pet_payload(pet)
        return Result.success(data=data, msg="查询成功").to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pk"])
        data = AdminPetCreateSerializer.build_pet_payload(pet)

        with transaction.atomic():
            PetGuide.objects.filter(pet_id=pet.id).delete()
            PetImage.objects.filter(pet_id=pet.id).delete()
            PetsAttribute.objects.filter(pet_id=pet.id).delete()
            PetsEggGroup.objects.filter(pet_id=pet.id).delete()
            PetsPetFeature.objects.filter(pet_id=pet.id).delete()
            PetsPetGeneration.objects.filter(pet_id=pet.id).delete()
            PetsPetGuide.objects.filter(pet_id=pet.id).delete()
            PetsPetRance.objects.filter(pet_id=pet.id).delete()
            PetsPetRegion.objects.filter(pet_id=pet.id).delete()
            PetsPetSkill.objects.filter(pet_id=pet.id).delete()
            PetsTag.objects.filter(pet_id=pet.id).delete()
            pet.delete()

        return Result.success(data=data, msg="删除成功").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        pet = self._get_pet(kwargs["pk"])
        serializer = AdminPetUpdateSerializer(
            pet,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Result.success(data=data, msg="修改成功").to_response()

    @staticmethod
    def _get_pet(pk: int) -> Pets:
        return get_object_or_404(Pets, pk=pk)
