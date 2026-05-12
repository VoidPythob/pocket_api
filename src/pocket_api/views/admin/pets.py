from typing import Any

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.enums import ResponseCode
from pocket_api.models import (
    PetEggGroup,
    PetFeature,
    PetGeneration,
    PetRance,
    Pets,
    PetsEggGroup,
    PetsPetFeature,
    PetsPetGeneration,
    PetsPetRance,
)
from pocket_api.result import Result
from pocket_api.serializers import (
    AdminPetCreateSerializer,
    AdminPetEggGroupRelationCreateSerializer,
    AdminPetEggGroupRelationUpdateSerializer,
    AdminPetEggGroupSerializer,
    AdminPetFeatureSerializer,
    AdminPetGenerationRelationCreateSerializer,
    AdminPetGenerationRelationUpdateSerializer,
    AdminPetRanceRelationCreateSerializer,
    AdminPetRanceRelationUpdateSerializer,
)


class AdminPetCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetCreateSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        pet = serializer.save()
        return Result.created(data=pet, msg="创建宠物成功").to_response()


class AdminPetEggGroupView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            egg_group = get_object_or_404(PetEggGroup, pk=pk)
            serializer = AdminPetEggGroupSerializer(egg_group)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = PetEggGroup.objects.all().order_by("-id")
        serializer = AdminPetEggGroupSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetEggGroupSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        egg_group = serializer.save()
        return Result.created(
            data=AdminPetEggGroupSerializer(egg_group).data, msg="创建成功"
        ).to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: Any):
        return self._update(request, *args, partial=True, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        egg_group = get_object_or_404(PetEggGroup, pk=kwargs["pk"])
        if PetsEggGroup.objects.filter(egg_group_id=egg_group.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT,
                msg="该蛋组已被宠物关联，不能删除",
            ).to_response()

        data = AdminPetEggGroupSerializer(egg_group).data
        egg_group.delete()
        return Result.success(data=data, msg="删除成功").to_response()

    def _update(
        self, request: Request, *args: Any, partial: bool = False, **kwargs: Any
    ):
        egg_group = get_object_or_404(PetEggGroup, pk=kwargs["pk"])
        serializer = AdminPetEggGroupSerializer(
            egg_group,
            data=request.data,
            partial=partial,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        egg_group = serializer.save()
        return Result.success(
            data=AdminPetEggGroupSerializer(egg_group).data, msg="修改成功"
        ).to_response()


class AdminPetFeatureView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pk = kwargs.get("pk")
        if pk is not None:
            feature = get_object_or_404(PetFeature, pk=pk)
            serializer = AdminPetFeatureSerializer(feature)
            return Result.success(data=serializer.data, msg="查询成功").to_response()

        queryset = PetFeature.objects.all().order_by("-id")
        serializer = AdminPetFeatureSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        serializer = AdminPetFeatureSerializer(
            data=request.data,
            context={"admin_user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        feature = serializer.save()
        return Result.created(
            data=AdminPetFeatureSerializer(feature).data, msg="创建成功"
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
                msg="该特性已被宠物关联，不能删除",
            ).to_response()

        data = AdminPetFeatureSerializer(feature).data
        feature.delete()
        return Result.success(data=data, msg="删除成功").to_response()

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
            data=AdminPetFeatureSerializer(feature).data, msg="修改成功"
        ).to_response()


class AdminPetRanceRelationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        relations = list(PetsPetRance.objects.filter(pet_id=pet.id))
        rance_ids = [relation.rance_id for relation in relations]
        rance_map = {
            item.id: item
            for item in PetRance.objects.filter(id__in=rance_ids, is_delete=0)
        }
        data = {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "rances": [
                self._build_rance_payload(pet, rance_map[relation.rance_id])
                for relation in relations
                if relation.rance_id in rance_map
            ],
        }
        return Result.success(data=data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        serializer = AdminPetRanceRelationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rance = self._get_rance(serializer.validated_data["rance_id"])

        if PetsPetRance.objects.filter(pet_id=pet.id, rance_id=rance.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT, msg="该宠物和种族已存在关联"
            ).to_response()

        PetsPetRance.objects.create(pet_id=pet.id, rance_id=rance.id)
        data = self._build_rance_payload(pet, rance)
        return Result.created(data=data, msg="关联成功").to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        old_rance = self._get_pet_relation_rance(pet.id, kwargs["rance_id"])
        serializer = AdminPetRanceRelationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_rance = self._get_rance(serializer.validated_data["new_rance_id"])

        if old_rance.id == new_rance.id:
            return Result.success(
                data=self._build_rance_payload(pet, old_rance), msg="修改成功"
            ).to_response()

        if PetsPetRance.objects.filter(pet_id=pet.id, rance_id=new_rance.id).exists():
            return Result.from_code(
                ResponseCode.CONFLICT, msg="该宠物和目标种族已存在关联"
            ).to_response()

        with transaction.atomic():
            PetsPetRance.objects.filter(pet_id=pet.id, rance_id=old_rance.id).delete()
            PetsPetRance.objects.create(pet_id=pet.id, rance_id=new_rance.id)

        return Result.success(
            data=self._build_rance_payload(pet, new_rance), msg="修改成功"
        ).to_response()

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        rance = self._get_pet_relation_rance(pet.id, kwargs["rance_id"])
        PetsPetRance.objects.filter(pet_id=pet.id, rance_id=rance.id).delete()
        return Result.success(
            data=self._build_rance_payload(pet, rance), msg="解除关联成功"
        ).to_response()

    @staticmethod
    def _get_pet(pk: int) -> Pets:
        return get_object_or_404(Pets, pk=pk)

    @staticmethod
    def _get_rance(pk: int) -> PetRance:
        return get_object_or_404(PetRance, pk=pk, is_delete=0)

    def _get_pet_relation_rance(self, pet_id: int, rance_id: int) -> PetRance:
        relation = get_object_or_404(PetsPetRance, pet_id=pet_id, rance_id=rance_id)
        return self._get_rance(relation.rance_id)

    @staticmethod
    def _build_rance_payload(pet: Pets, rance: PetRance) -> dict[str, Any]:
        return {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "rance_id": rance.id,
            "rance_name": rance.name,
        }


class AdminPetEggGroupRelationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        relations = list(PetsEggGroup.objects.filter(pet_id=pet.id))
        egg_group_ids = [relation.egg_group_id for relation in relations]
        egg_group_map = {
            item.id: item for item in PetEggGroup.objects.filter(id__in=egg_group_ids)
        }
        data = {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "egg_groups": [
                self._build_egg_group_payload(pet, egg_group_map[relation.egg_group_id])
                for relation in relations
                if relation.egg_group_id in egg_group_map
            ],
        }
        return Result.success(data=data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        serializer = AdminPetEggGroupRelationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        egg_group = self._get_egg_group(serializer.validated_data["egg_group_id"])

        if PetsEggGroup.objects.filter(
            pet_id=pet.id, egg_group_id=egg_group.id
        ).exists():
            return Result.from_code(
                ResponseCode.CONFLICT, msg="该宠物和蛋组已存在关联"
            ).to_response()

        PetsEggGroup.objects.create(pet_id=pet.id, egg_group_id=egg_group.id)
        data = self._build_egg_group_payload(pet, egg_group)
        return Result.created(data=data, msg="关联成功").to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        old_egg_group = self._get_pet_relation_egg_group(pet.id, kwargs["egg_group_id"])
        serializer = AdminPetEggGroupRelationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_egg_group = self._get_egg_group(
            serializer.validated_data["new_egg_group_id"]
        )

        if old_egg_group.id == new_egg_group.id:
            return Result.success(
                data=self._build_egg_group_payload(pet, old_egg_group), msg="修改成功"
            ).to_response()

        if PetsEggGroup.objects.filter(
            pet_id=pet.id, egg_group_id=new_egg_group.id
        ).exists():
            return Result.from_code(
                ResponseCode.CONFLICT, msg="该宠物和目标蛋组已存在关联"
            ).to_response()

        with transaction.atomic():
            PetsEggGroup.objects.filter(
                pet_id=pet.id, egg_group_id=old_egg_group.id
            ).delete()
            PetsEggGroup.objects.create(
                pet_id=pet.id, egg_group_id=new_egg_group.id
            )

        return Result.success(
            data=self._build_egg_group_payload(pet, new_egg_group), msg="修改成功"
        ).to_response()

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        egg_group = self._get_pet_relation_egg_group(pet.id, kwargs["egg_group_id"])
        PetsEggGroup.objects.filter(pet_id=pet.id, egg_group_id=egg_group.id).delete()
        return Result.success(
            data=self._build_egg_group_payload(pet, egg_group), msg="解除关联成功"
        ).to_response()

    @staticmethod
    def _get_pet(pk: int) -> Pets:
        return get_object_or_404(Pets, pk=pk)

    @staticmethod
    def _get_egg_group(pk: int) -> PetEggGroup:
        return get_object_or_404(PetEggGroup, pk=pk)

    def _get_pet_relation_egg_group(
        self, pet_id: int, egg_group_id: int
    ) -> PetEggGroup:
        relation = get_object_or_404(
            PetsEggGroup, pet_id=pet_id, egg_group_id=egg_group_id
        )
        return self._get_egg_group(relation.egg_group_id)

    @staticmethod
    def _build_egg_group_payload(
        pet: Pets, egg_group: PetEggGroup
    ) -> dict[str, Any]:
        return {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "egg_group_id": egg_group.id,
            "egg_group_name": egg_group.name,
        }


class AdminPetGenerationRelationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        relations = list(PetsPetGeneration.objects.filter(pet_id=pet.id))
        generation_ids = [relation.generation_id for relation in relations]
        generation_map = {
            item.id: item
            for item in PetGeneration.objects.filter(id__in=generation_ids)
        }
        data = {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "generations": [
                self._build_generation_payload(
                    pet, generation_map[relation.generation_id]
                )
                for relation in relations
                if relation.generation_id in generation_map
            ],
        }
        return Result.success(data=data, msg="查询成功").to_response()

    def post(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        serializer = AdminPetGenerationRelationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        generation = self._get_generation(serializer.validated_data["generation_id"])

        if PetsPetGeneration.objects.filter(
            pet_id=pet.id, generation_id=generation.id
        ).exists():
            return Result.from_code(
                ResponseCode.CONFLICT, msg="该宠物和世代已存在关联"
            ).to_response()

        PetsPetGeneration.objects.create(pet_id=pet.id, generation_id=generation.id)
        data = self._build_generation_payload(pet, generation)
        return Result.created(data=data, msg="关联成功").to_response()

    def put(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        old_generation = self._get_pet_relation_generation(
            pet.id, kwargs["generation_id"]
        )
        serializer = AdminPetGenerationRelationUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_generation = self._get_generation(
            serializer.validated_data["new_generation_id"]
        )

        if old_generation.id == new_generation.id:
            return Result.success(
                data=self._build_generation_payload(pet, old_generation), msg="修改成功"
            ).to_response()

        if PetsPetGeneration.objects.filter(
            pet_id=pet.id, generation_id=new_generation.id
        ).exists():
            return Result.from_code(
                ResponseCode.CONFLICT, msg="该宠物和目标世代已存在关联"
            ).to_response()

        with transaction.atomic():
            PetsPetGeneration.objects.filter(
                pet_id=pet.id, generation_id=old_generation.id
            ).delete()
            PetsPetGeneration.objects.create(
                pet_id=pet.id, generation_id=new_generation.id
            )

        return Result.success(
            data=self._build_generation_payload(pet, new_generation), msg="修改成功"
        ).to_response()

    def delete(self, request: Request, *args: Any, **kwargs: Any):
        pet = self._get_pet(kwargs["pet_id"])
        generation = self._get_pet_relation_generation(pet.id, kwargs["generation_id"])
        PetsPetGeneration.objects.filter(
            pet_id=pet.id, generation_id=generation.id
        ).delete()
        return Result.success(
            data=self._build_generation_payload(pet, generation), msg="解除关联成功"
        ).to_response()

    @staticmethod
    def _get_pet(pk: int) -> Pets:
        return get_object_or_404(Pets, pk=pk)

    @staticmethod
    def _get_generation(pk: int) -> PetGeneration:
        return get_object_or_404(PetGeneration, pk=pk)

    def _get_pet_relation_generation(
        self, pet_id: int, generation_id: int
    ) -> PetGeneration:
        relation = get_object_or_404(
            PetsPetGeneration, pet_id=pet_id, generation_id=generation_id
        )
        return self._get_generation(relation.generation_id)

    @staticmethod
    def _build_generation_payload(
        pet: Pets, generation: PetGeneration
    ) -> dict[str, Any]:
        return {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "generation_id": generation.id,
            "generation_name": generation.name,
        }
