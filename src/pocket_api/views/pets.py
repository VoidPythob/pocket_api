from __future__ import annotations

from typing import Any

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.views import APIView

from pocket_api.models import (
    PetCaptureMethod,
    PetEggGroup,
    PetFeature,
    PetImage,
    PetRance,
    PetRegion,
    PetSkill,
    Pets,
    PetsEggGroup,
    PetsPetFeature,
    PetsPetGeneration,
    PetsPetRance,
    PetsPetRegion,
    PetsPetSkill,
    PetsTag,
    Tag,
)
from pocket_api.result import Result
from pocket_api.serializers import (
    PetCaptureMethodPayloadSerializer,
    PetDetailSerializer,
    PetFeatureListQuerySerializer,
    PetFeaturePayloadSerializer,
    PetListItemSerializer,
    PetListQuerySerializer,
    PetsSerializer,
)

from .pet_payloads import build_pet_list_payload


class PetsView(viewsets.ReadOnlyModelViewSet[Pets]):
    queryset = Pets.objects.all().order_by("-id")
    serializer_class = PetsSerializer
    http_method_names = ["get", "head", "options"]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def list(self, request: Request, *args: Any, **kwargs: Any):
        query_serializer = PetListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        generation_id = query_serializer.validated_data["generation_id"]
        feature_id = query_serializer.validated_data.get("feature_id")
        name = query_serializer.validated_data.get("name")

        pet_ids = PetsPetGeneration.objects.filter(generation_id=generation_id).values_list(
            "pet_id", flat=True
        )
        queryset = self.get_queryset().filter(id__in=pet_ids)
        if feature_id:
            feature_pet_ids = PetsPetFeature.objects.filter(
                feature_id=feature_id
            ).values_list("pet_id", flat=True)
            queryset = queryset.filter(id__in=feature_pet_ids)
        if name:
            queryset = queryset.filter(name__icontains=name)

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = build_pet_list_payload(page)
            serializer = PetListItemSerializer(data, many=True)
            return Result.success(
                data={
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "results": serializer.data,
                },
                msg="查询成功",
            ).to_response()

        data = build_pet_list_payload(queryset)
        serializer = PetListItemSerializer(data, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def retrieve(self, request: Request, *args: Any, **kwargs: Any):
        instance = self.get_object()
        serializer = PetDetailSerializer(self._build_detail_payload(instance))
        return Result.success(data=serializer.data, msg="查询成功").to_response()

    def get_queryset(self) -> models.QuerySet[Pets]:
        return self.queryset

    @staticmethod
    def _build_detail_payload(pet: Pets) -> dict[str, Any]:
        images = list(PetImage.objects.filter(pet_id=pet.id).order_by("sort", "id"))
        feature_relations = list(PetsPetFeature.objects.filter(pet_id=pet.id))
        feature_ids = [relation.feature_id for relation in feature_relations]
        feature_map = {
            feature.id: feature
            for feature in PetFeature.objects.filter(id__in=feature_ids)
        }
        tag_relations = list(PetsTag.objects.filter(pet_id=pet.id))
        tag_ids = [relation.tag_id for relation in tag_relations]
        tag_map = {tag.id: tag for tag in Tag.objects.filter(id__in=tag_ids)}
        egg_group_relations = list(PetsEggGroup.objects.filter(pet_id=pet.id))
        egg_group_ids = [relation.egg_group_id for relation in egg_group_relations]
        egg_group_map = {
            item.id: item for item in PetEggGroup.objects.filter(id__in=egg_group_ids)
        }
        rance_relations = list(PetsPetRance.objects.filter(pet_id=pet.id))
        rance_ids = [relation.rance_id for relation in rance_relations]
        rance_map = {
            item.id: item
            for item in PetRance.objects.filter(id__in=rance_ids, is_delete=0)
        }
        skill_relations = list(PetsPetSkill.objects.filter(pet_id=pet.id))
        skill_ids = [relation.skill_id for relation in skill_relations]
        skill_map = {
            item.id: item for item in PetSkill.objects.filter(id__in=skill_ids)
        }

        first_image_url = images[0].image_url if images else None
        gender_ratio_display = PetsView._build_gender_ratio_display(
            pet.gender_male_ratio
        )

        return {
            "id": pet.id,
            "name": pet.name,
            "jp_name": pet.jp_name,
            "en_name": pet.en_name,
            "weight": pet.weight,
            "gender_male_ratio": pet.gender_male_ratio,
            "gender_ratio_display": gender_ratio_display,
            "base_point_type": pet.base_point_type,
            "base_point_value": pet.base_point_value,
            "capture_probability": pet.capture_probability,
            "egg_hatching_steps": pet.egg_hatching_steps,
            "first_image_url": first_image_url,
            "images": [
                {
                    "id": image.id,
                    "image_url": image.image_url,
                    "sort": image.sort,
                    "is_cover": image.is_cover,
                }
                for image in images
            ],
            "tags": [
                {
                    "id": tag_map[relation.tag_id].id,
                    "name": tag_map[relation.tag_id].name,
                    "color": tag_map[relation.tag_id].color,
                }
                for relation in tag_relations
                if relation.tag_id in tag_map
            ],
            "egg_groups": [
                {
                    "id": egg_group_map[relation.egg_group_id].id,
                    "name": egg_group_map[relation.egg_group_id].name,
                }
                for relation in egg_group_relations
                if relation.egg_group_id in egg_group_map
            ],
            "features": [
                {
                    "id": feature_map[relation.feature_id].id,
                    "introduction": feature_map[relation.feature_id].introduction,
                    "detail": feature_map[relation.feature_id].detail,
                }
                for relation in feature_relations
                if relation.feature_id in feature_map
            ],
            "rances": [
                {
                    "id": rance_map[relation.rance_id].id,
                    "name": rance_map[relation.rance_id].name,
                    "hp": rance_map[relation.rance_id].hp,
                    "attack": rance_map[relation.rance_id].attack,
                    "defense": rance_map[relation.rance_id].defense,
                    "special_attack": rance_map[relation.rance_id].special_attack,
                    "special_defense": rance_map[relation.rance_id].special_defense,
                    "speed": rance_map[relation.rance_id].speed,
                    "total": rance_map[relation.rance_id].total,
                }
                for relation in rance_relations
                if relation.rance_id in rance_map
            ],
            "skills": [
                {
                    "id": skill_map[relation.skill_id].id,
                    "learn_type": skill_map[relation.skill_id].learn_type,
                    "category_id": skill_map[relation.skill_id].category_id,
                    "attribute_id": skill_map[relation.skill_id].attribute_id,
                    "name": skill_map[relation.skill_id].name,
                    "introduction": skill_map[relation.skill_id].introduction,
                    "detail": skill_map[relation.skill_id].detail,
                    "damage": skill_map[relation.skill_id].damage,
                    "aim": skill_map[relation.skill_id].aim,
                    "pp": skill_map[relation.skill_id].pp,
                    "cost_time": skill_map[relation.skill_id].cost_time,
                }
                for relation in skill_relations
                if relation.skill_id in skill_map
            ],
            "create_by": pet.create_by,
            "modified_by": pet.modified_by,
            "create_at": pet.create_at,
            "modified_at": pet.modified_at,
        }

    @staticmethod
    def _build_gender_ratio_display(gender_male_ratio: int | None) -> str | None:
        if gender_male_ratio is None:
            return None

        male_ratio = float(gender_male_ratio)
        female_ratio = 100.0 - male_ratio
        return f"{{woman}}{female_ratio:.1f} / {{man}}{male_ratio:.1f}"


class PetFeaturesView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any):
        pet = get_object_or_404(Pets, pk=kwargs["pk"])
        relations = list(PetsPetFeature.objects.filter(pet_id=pet.id))
        feature_ids = [relation.feature_id for relation in relations]
        feature_map = {
            feature.id: feature
            for feature in PetFeature.objects.filter(id__in=feature_ids)
        }
        data = {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "features": [
                {
                    "id": feature_map[relation.feature_id].id,
                    "introduction": feature_map[relation.feature_id].introduction,
                    "detail": feature_map[relation.feature_id].detail,
                }
                for relation in relations
                if relation.feature_id in feature_map
            ],
        }
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(data["features"], request)
        if page is not None:
            serializer = PetFeaturePayloadSerializer(page, many=True)
            data["features"] = {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": serializer.data,
            }
            return Result.success(data=data, msg="查询成功").to_response()

        serializer = PetFeaturePayloadSerializer(data["features"], many=True)
        data["features"] = serializer.data
        return Result.success(data=data, msg="查询成功").to_response()


class PetCaptureMethodsView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any):
        pet = get_object_or_404(Pets, pk=kwargs["pk"])
        region_relations = list(PetsPetRegion.objects.filter(pet_id=pet.id))
        region_ids = [relation.region_id for relation in region_relations]
        region_map = {
            region.id: region for region in PetRegion.objects.filter(id__in=region_ids)
        }
        methods = list(
            PetCaptureMethod.objects.filter(pet_region_id__in=region_ids).order_by(
                "pet_region_id", "id"
            )
        )
        data = {
            "pet_id": pet.id,
            "pet_name": pet.name,
            "capture_methods": [
                {
                    "id": method.id,
                    "pet_region_id": method.pet_region_id,
                    "region_name": region_map[method.pet_region_id].name
                    if method.pet_region_id in region_map
                    else None,
                    "method": method.method,
                    "detail": method.detail,
                }
                for method in methods
            ],
        }
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(data["capture_methods"], request)
        if page is not None:
            serializer = PetCaptureMethodPayloadSerializer(page, many=True)
            data["capture_methods"] = {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": serializer.data,
            }
            return Result.success(data=data, msg="查询成功").to_response()

        serializer = PetCaptureMethodPayloadSerializer(
            data["capture_methods"], many=True
        )
        data["capture_methods"] = serializer.data
        return Result.success(data=data, msg="查询成功").to_response()


class PetFeatureDetailView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any):
        feature = get_object_or_404(PetFeature, pk=kwargs["pk"])
        data = {
            "id": feature.id,
            "introduction": feature.introduction,
            "detail": feature.detail,
        }
        serializer = PetFeaturePayloadSerializer(data)
        return Result.success(data=serializer.data, msg="查询成功").to_response()


class PetFeatureListView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any):
        query_serializer = PetFeatureListQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        name = query_serializer.validated_data.get("name")

        queryset = PetFeature.objects.all().order_by("-id")
        if name:
            queryset = queryset.filter(introduction__icontains=name)

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PetFeaturePayloadSerializer(page, many=True)
            return Result.success(
                data={
                    "count": paginator.page.paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "results": serializer.data,
                },
                msg="查询成功",
            ).to_response()

        serializer = PetFeaturePayloadSerializer(queryset, many=True)
        return Result.success(data=serializer.data, msg="查询成功").to_response()


class PetCaptureMethodDetailView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any):
        capture_method = get_object_or_404(PetCaptureMethod, pk=kwargs["pk"])
        region = None
        if capture_method.pet_region_id is not None:
            region = PetRegion.objects.filter(pk=capture_method.pet_region_id).first()

        data = {
            "id": capture_method.id,
            "pet_region_id": capture_method.pet_region_id,
            "region_name": region.name if region is not None else None,
            "method": capture_method.method,
            "detail": capture_method.detail,
        }
        serializer = PetCaptureMethodPayloadSerializer(data)
        return Result.success(data=serializer.data, msg="查询成功").to_response()
