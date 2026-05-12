from __future__ import annotations

from typing import Any

from django.db import models

from pocket_api.models import PetFeature, PetImage, Pets, PetsPetFeature, PetsTag, Tag


def build_pet_list_payload(
    pets: list[Pets] | models.QuerySet[Pets],
) -> list[dict[str, Any]]:
    pet_list = list(pets)
    pet_ids = [pet.id for pet in pet_list]
    if not pet_ids:
        return []

    image_map: dict[int, str | None] = {}
    for image in PetImage.objects.filter(pet_id__in=pet_ids).order_by(
        "pet_id", "sort", "id"
    ):
        image_map.setdefault(image.pet_id, image.image_url)

    feature_relations = list(PetsPetFeature.objects.filter(pet_id__in=pet_ids))
    feature_ids = [relation.feature_id for relation in feature_relations]
    feature_map = {
        feature.id: feature for feature in PetFeature.objects.filter(id__in=feature_ids)
    }

    tag_relations = list(PetsTag.objects.filter(pet_id__in=pet_ids))
    tag_ids = [relation.tag_id for relation in tag_relations]
    tag_map = {tag.id: tag for tag in Tag.objects.filter(id__in=tag_ids)}

    pet_features_map: dict[int, list[dict[str, Any]]] = {
        pet_id: [] for pet_id in pet_ids
    }
    pet_tags_map: dict[int, list[dict[str, Any]]] = {pet_id: [] for pet_id in pet_ids}

    for relation in feature_relations:
        feature = feature_map.get(relation.feature_id)
        if feature is None:
            continue
        pet_features_map.setdefault(relation.pet_id, []).append(
            {
                "id": feature.id,
                "introduction": feature.introduction,
                "detail": feature.detail,
            }
        )

    for relation in tag_relations:
        tag = tag_map.get(relation.tag_id)
        if tag is None:
            continue
        pet_tags_map.setdefault(relation.pet_id, []).append(
            {
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
            }
        )

    return [
        {
            "id": pet.id,
            "name": pet.name,
            "jp_name": pet.jp_name,
            "en_name": pet.en_name,
            "first_image_url": image_map.get(pet.id),
            "tags": pet_tags_map.get(pet.id, []),
            "features": pet_features_map.get(pet.id, []),
        }
        for pet in pet_list
    ]
