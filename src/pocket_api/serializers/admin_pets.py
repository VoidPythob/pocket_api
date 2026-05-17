from __future__ import annotations

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from pocket_api.models import (
    PetEggGroup,
    PetFeature,
    PetGeneration,
    PetImage,
    PetRance,
    PetSkill,
    PetsEggGroup,
    PetsTag,
    Pets,
    PetsPetFeature,
    PetsPetGeneration,
    PetsPetRance,
    PetsPetSkill,
    Tag,
)


class AdminPetCreateSerializer(serializers.Serializer):
    icon_urls = serializers.ListField(
        child=serializers.URLField(max_length=255),
        allow_empty=True,
        write_only=True,
    )
    name = serializers.CharField(max_length=100)
    jp_name = serializers.CharField(max_length=100)
    en_name = serializers.CharField(max_length=100)
    gender_male_ratio = serializers.IntegerField(
        min_value=0, max_value=100, required=False, allow_null=True
    )
    feature_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        write_only=True,
    )
    generation_id = serializers.IntegerField(min_value=1, write_only=True)
    rance_id = serializers.IntegerField(min_value=1, write_only=True)
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        write_only=True,
    )
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        write_only=True,
        required=False,
    )
    egg_group_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        write_only=True,
        required=False,
    )

    def validate_name(self, value: str) -> str:
        if Pets.objects.filter(name=value).exists():
            raise serializers.ValidationError("pet name already exists")
        return value

    def validate(self, attrs: dict[str, object]) -> dict[str, object]:
        attrs["icon_urls"] = list(dict.fromkeys(attrs["icon_urls"]))  # type: ignore[index]
        attrs["feature_ids"] = list(dict.fromkeys(attrs["feature_ids"]))  # type: ignore[index]
        attrs["skill_ids"] = list(dict.fromkeys(attrs["skill_ids"]))  # type: ignore[index]
        attrs["tag_ids"] = list(dict.fromkeys(attrs.get("tag_ids", [])))  # type: ignore[arg-type]
        attrs["egg_group_ids"] = list(dict.fromkeys(attrs.get("egg_group_ids", [])))  # type: ignore[arg-type]

        self._ensure_ids_exist(
            model=PetFeature,
            ids=attrs["feature_ids"],  # type: ignore[arg-type]
            error_prefix="feature",
        )
        self._ensure_ids_exist(
            model=PetSkill,
            ids=attrs["skill_ids"],  # type: ignore[arg-type]
            error_prefix="skill",
        )
        self._ensure_ids_exist(
            model=PetGeneration,
            ids=[attrs["generation_id"]],  # type: ignore[list-item]
            error_prefix="generation",
        )
        self._ensure_ids_exist(
            model=PetRance,
            ids=[attrs["rance_id"]],  # type: ignore[list-item]
            error_prefix="rance",
        )
        self._ensure_ids_exist(
            model=Tag,
            ids=attrs["tag_ids"],  # type: ignore[arg-type]
            error_prefix="tag",
        )
        self._ensure_ids_exist(
            model=PetEggGroup,
            ids=attrs["egg_group_ids"],  # type: ignore[arg-type]
            error_prefix="egg group",
        )
        return attrs

    def create(self, validated_data: dict[str, object]) -> dict[str, object]:
        now = timezone.now()
        admin_user = self.context["admin_user"]
        icon_urls = list(validated_data.pop("icon_urls"))
        feature_ids = list(validated_data.pop("feature_ids"))
        skill_ids = list(validated_data.pop("skill_ids"))
        tag_ids = list(validated_data.pop("tag_ids", []))
        egg_group_ids = list(validated_data.pop("egg_group_ids", []))
        generation_id = int(validated_data.pop("generation_id"))
        rance_id = int(validated_data.pop("rance_id"))

        with transaction.atomic():
            pet = Pets.objects.create(
                **validated_data,
                weight=0,
                create_by=admin_user.id,
                create_at=now,
            )
            self._replace_images(
                pet_id=pet.id, icon_urls=icon_urls, admin_user_id=admin_user.id, now=now
            )
            self._replace_features(pet_id=pet.id, feature_ids=feature_ids)
            PetsPetGeneration.objects.create(pet_id=pet.id, generation_id=generation_id)
            PetsPetRance.objects.create(pet_id=pet.id, rance_id=rance_id)
            self._replace_skills(pet_id=pet.id, skill_ids=skill_ids)
            self._replace_tags(pet_id=pet.id, tag_ids=tag_ids)
            self._replace_egg_groups(pet_id=pet.id, egg_group_ids=egg_group_ids)

        return self.build_pet_payload(pet)

    @staticmethod
    def build_pet_payload(pet: Pets) -> dict[str, object]:
        generation_id = (
            PetsPetGeneration.objects.filter(pet_id=pet.id)
            .values_list("generation_id", flat=True)
            .first()
        )
        rance_id = (
            PetsPetRance.objects.filter(pet_id=pet.id)
            .values_list("rance_id", flat=True)
            .first()
        )
        return {
            "id": pet.id,
            "name": pet.name,
            "jp_name": pet.jp_name,
            "en_name": pet.en_name,
            "gender_male_ratio": pet.gender_male_ratio,
            "icon_urls": list(
                PetImage.objects.filter(pet_id=pet.id)
                .order_by("sort", "image_url")
                .values_list("image_url", flat=True)
            ),
            "feature_ids": list(
                PetsPetFeature.objects.filter(pet_id=pet.id)
                .order_by("feature_id")
                .values_list("feature_id", flat=True)
            ),
            "generation_id": generation_id,
            "rance_id": rance_id,
            "skill_ids": list(
                PetsPetSkill.objects.filter(pet_id=pet.id)
                .order_by("skill_id")
                .values_list("skill_id", flat=True)
            ),
            "tag_ids": list(
                PetsTag.objects.filter(pet_id=pet.id)
                .order_by("tag_id")
                .values_list("tag_id", flat=True)
            ),
            "egg_group_ids": list(
                PetsEggGroup.objects.filter(pet_id=pet.id)
                .order_by("egg_group_id")
                .values_list("egg_group_id", flat=True)
            ),
        }

    @staticmethod
    def _ensure_ids_exist(*, model, ids: list[int], error_prefix: str) -> None:
        if not ids:
            return

        queryset = model.objects.filter(id__in=ids)
        if hasattr(model, "is_delete"):
            queryset = queryset.filter(is_delete=0)

        existing_ids = set(queryset.values_list("id", flat=True))
        missing_ids = sorted(set(ids) - existing_ids)
        if missing_ids:
            missing = ", ".join(str(item) for item in missing_ids)
            raise serializers.ValidationError(f"{error_prefix} not found: {missing}")

    @staticmethod
    def _replace_images(
        *, pet_id: int, icon_urls: list[str], admin_user_id: int, now
    ) -> None:
        PetImage.objects.filter(pet_id=pet_id).delete()
        PetImage.objects.bulk_create(
            [
                PetImage(
                    pet_id=pet_id,
                    image_url=image_url,
                    sort=index,
                    is_cover=1 if index == 0 else 0,
                    create_by=admin_user_id,
                    modified_by=admin_user_id,
                    create_at=now,
                    modified_at=now,
                )
                for index, image_url in enumerate(icon_urls)
            ]
        )

    @staticmethod
    def _replace_features(*, pet_id: int, feature_ids: list[int]) -> None:
        PetsPetFeature.objects.filter(pet_id=pet_id).delete()
        if not feature_ids:
            return

        PetsPetFeature.objects.bulk_create(
            [
                PetsPetFeature(pet_id=pet_id, feature_id=feature_id)
                for feature_id in feature_ids
            ]
        )

    @staticmethod
    def _replace_skills(*, pet_id: int, skill_ids: list[int]) -> None:
        PetsPetSkill.objects.filter(pet_id=pet_id).delete()
        if not skill_ids:
            return

        PetsPetSkill.objects.bulk_create(
            [PetsPetSkill(pet_id=pet_id, skill_id=skill_id) for skill_id in skill_ids]
        )

    @staticmethod
    def _replace_tags(*, pet_id: int, tag_ids: list[int]) -> None:
        PetsTag.objects.filter(pet_id=pet_id).delete()
        if not tag_ids:
            return

        PetsTag.objects.bulk_create(
            [PetsTag(pet_id=pet_id, tag_id=tag_id) for tag_id in tag_ids]
        )

    @staticmethod
    def _replace_egg_groups(*, pet_id: int, egg_group_ids: list[int]) -> None:
        PetsEggGroup.objects.filter(pet_id=pet_id).delete()
        if not egg_group_ids:
            return

        PetsEggGroup.objects.bulk_create(
            [
                PetsEggGroup(pet_id=pet_id, egg_group_id=egg_group_id)
                for egg_group_id in egg_group_ids
            ]
        )


class AdminPetUpdateSerializer(AdminPetCreateSerializer):
    def validate_name(self, value: str) -> str:
        queryset = Pets.objects.filter(name=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("pet name already exists")
        return value

    def validate(self, attrs: dict[str, object]) -> dict[str, object]:
        if "icon_urls" in attrs:
            attrs["icon_urls"] = list(dict.fromkeys(attrs["icon_urls"]))  # type: ignore[index]
        if "feature_ids" in attrs:
            attrs["feature_ids"] = list(dict.fromkeys(attrs["feature_ids"]))  # type: ignore[index]
        if "skill_ids" in attrs:
            attrs["skill_ids"] = list(dict.fromkeys(attrs["skill_ids"]))  # type: ignore[index]
        if "tag_ids" in attrs:
            attrs["tag_ids"] = list(dict.fromkeys(attrs["tag_ids"]))  # type: ignore[index]
        if "egg_group_ids" in attrs:
            attrs["egg_group_ids"] = list(dict.fromkeys(attrs["egg_group_ids"]))  # type: ignore[index]

        if "feature_ids" in attrs:
            self._ensure_ids_exist(
                model=PetFeature,
                ids=attrs["feature_ids"],  # type: ignore[arg-type]
                error_prefix="feature",
            )
        if "skill_ids" in attrs:
            self._ensure_ids_exist(
                model=PetSkill,
                ids=attrs["skill_ids"],  # type: ignore[arg-type]
                error_prefix="skill",
            )
        if "generation_id" in attrs:
            self._ensure_ids_exist(
                model=PetGeneration,
                ids=[attrs["generation_id"]],  # type: ignore[list-item]
                error_prefix="generation",
            )
        if "rance_id" in attrs:
            self._ensure_ids_exist(
                model=PetRance,
                ids=[attrs["rance_id"]],  # type: ignore[list-item]
                error_prefix="rance",
            )
        if "tag_ids" in attrs:
            self._ensure_ids_exist(
                model=Tag,
                ids=attrs["tag_ids"],  # type: ignore[arg-type]
                error_prefix="tag",
            )
        if "egg_group_ids" in attrs:
            self._ensure_ids_exist(
                model=PetEggGroup,
                ids=attrs["egg_group_ids"],  # type: ignore[arg-type]
                error_prefix="egg group",
            )
        return attrs

    def update(
        self, instance: Pets, validated_data: dict[str, object]
    ) -> dict[str, object]:
        now = timezone.now()
        admin_user = self.context["admin_user"]
        icon_urls = validated_data.pop("icon_urls", None)
        feature_ids = validated_data.pop("feature_ids", None)
        generation_id = validated_data.pop("generation_id", None)
        rance_id = validated_data.pop("rance_id", None)
        skill_ids = validated_data.pop("skill_ids", None)
        tag_ids = validated_data.pop("tag_ids", None)
        egg_group_ids = validated_data.pop("egg_group_ids", None)

        with transaction.atomic():
            update_fields = ["modified_by", "modified_at"]
            for field in ("name", "jp_name", "en_name", "gender_male_ratio"):
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
                    update_fields.append(field)

            instance.modified_by = admin_user.id
            instance.modified_at = now
            instance.save(update_fields=update_fields)

            if icon_urls is not None:
                self._replace_images(
                    pet_id=instance.id,
                    icon_urls=list(icon_urls),
                    admin_user_id=admin_user.id,
                    now=now,
                )
            if feature_ids is not None:
                self._replace_features(
                    pet_id=instance.id,
                    feature_ids=list(feature_ids),
                )
            if generation_id is not None:
                PetsPetGeneration.objects.filter(pet_id=instance.id).delete()
                PetsPetGeneration.objects.create(
                    pet_id=instance.id,
                    generation_id=int(generation_id),
                )
            if rance_id is not None:
                PetsPetRance.objects.filter(pet_id=instance.id).delete()
                PetsPetRance.objects.create(
                    pet_id=instance.id,
                    rance_id=int(rance_id),
                )
            if skill_ids is not None:
                self._replace_skills(
                    pet_id=instance.id,
                    skill_ids=list(skill_ids),
                )
            if tag_ids is not None:
                self._replace_tags(
                    pet_id=instance.id,
                    tag_ids=list(tag_ids),
                )
            if egg_group_ids is not None:
                self._replace_egg_groups(
                    pet_id=instance.id,
                    egg_group_ids=list(egg_group_ids),
                )

        return self.build_pet_payload(instance)
