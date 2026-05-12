from __future__ import annotations

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from pocket_api.models import (
    AdminUser,
    GameDocs,
    ItemCategory,
    Items,
    PetEggGroup,
    PetFeature,
    PetGeneration,
    PetImage,
    PetRance,
    PetSkill,
    PetSkillCategory,
    Pets,
    PetsPetFeature,
    PetsPetGeneration,
    PetsPetRance,
    PetsPetSkill,
    Tag,
)


class AdminUserSerializer(serializers.ModelSerializer[AdminUser]):
    last_login_time = serializers.DateTimeField(source="last_login", read_only=True)

    class Meta:  # type: ignore
        model = AdminUser
        fields = ("id", "email", "last_login_ip", "last_login_time")


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(
        max_length=128, write_only=True, trim_whitespace=False
    )


class AdminRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(
        max_length=128, write_only=True, trim_whitespace=False
    )
    password_confirm = serializers.CharField(
        max_length=128, write_only=True, trim_whitespace=False
    )

    def validate_email(self, value: str) -> str:
        if AdminUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已存在")
        return value

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("两次密码不一致")
        self._ensure_ids_exist(
            model=PetGeneration,
            ids=[attrs["generation_id"]],  # type: ignore[list-item]
            error_prefix="世代",
        )
        self._ensure_ids_exist(
            model=PetGeneration,
            ids=[attrs["generation_id"]],  # type: ignore[list-item]
            error_prefix="世代",
        )
        return attrs

    def create(self, validated_data: dict[str, str]) -> AdminUser:
        validated_data.pop("password_confirm")
        return AdminUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            create_at=timezone.now(),
        )


class AdminPetCreateSerializer(serializers.Serializer):
    icon_urls = serializers.ListField(
        child=serializers.URLField(max_length=255),
        allow_empty=False,
        write_only=True,
    )
    name = serializers.CharField(max_length=100)
    jp_name = serializers.CharField(max_length=100)
    en_name = serializers.CharField(max_length=100)
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

    def validate_name(self, value: str) -> str:
        if Pets.objects.filter(name=value).exists():
            raise serializers.ValidationError("宠物名称已存在")
        return value

    def validate(self, attrs: dict[str, object]) -> dict[str, object]:
        attrs["icon_urls"] = list(dict.fromkeys(attrs["icon_urls"]))  # type: ignore[index]
        attrs["feature_ids"] = list(dict.fromkeys(attrs["feature_ids"]))  # type: ignore[index]
        attrs["skill_ids"] = list(dict.fromkeys(attrs["skill_ids"]))  # type: ignore[index]

        self._ensure_ids_exist(
            model=PetFeature,
            ids=attrs["feature_ids"],  # type: ignore[arg-type]
            error_prefix="特性",
        )
        self._ensure_ids_exist(
            model=PetSkill,
            ids=attrs["skill_ids"],  # type: ignore[arg-type]
            error_prefix="技能",
        )
        self._ensure_ids_exist(
            model=PetRance,
            ids=[attrs["rance_id"]],  # type: ignore[list-item]
            error_prefix="种族",
        )
        return attrs

    def create(self, validated_data: dict[str, object]) -> dict[str, object]:
        now = timezone.now()
        admin_user = self.context["admin_user"]
        icon_urls = validated_data.pop("icon_urls")
        feature_ids = validated_data.pop("feature_ids")
        skill_ids = validated_data.pop("skill_ids")
        generation_id = validated_data.pop("generation_id")
        rance_id = validated_data.pop("rance_id")

        with transaction.atomic():
            pet = Pets.objects.create(
                **validated_data,
                weight=0,
                create_by=admin_user.id,
                create_at=now,
            )

            PetImage.objects.bulk_create(
                [
                    PetImage(
                        pet_id=pet.id,
                        image_url=image_url,
                        sort=index,
                        is_cover=1 if index == 0 else 0,
                        create_by=admin_user.id,
                        create_at=now,
                    )
                    for index, image_url in enumerate(icon_urls)
                ]
            )

            if feature_ids:
                PetsPetFeature.objects.bulk_create(
                    [
                        PetsPetFeature(pet_id=pet.id, feature_id=feature_id)
                        for feature_id in feature_ids
                    ]
                )

            PetsPetGeneration.objects.create(
                pet_id=pet.id,
                generation_id=generation_id,
            )

            PetsPetRance.objects.create(pet_id=pet.id, rance_id=rance_id)

            if skill_ids:
                PetsPetSkill.objects.bulk_create(
                    [
                        PetsPetSkill(pet_id=pet.id, skill_id=skill_id)
                        for skill_id in skill_ids
                    ]
                )

        return {
            "id": pet.id,
            "name": pet.name,
            "jp_name": pet.jp_name,
            "en_name": pet.en_name,
            "icon_urls": icon_urls,
            "feature_ids": feature_ids,
            "generation_id": generation_id,
            "rance_id": rance_id,
            "skill_ids": skill_ids,
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
            raise serializers.ValidationError(
                f"{error_prefix}不存在: {', '.join(str(item) for item in missing_ids)}"
            )


class AdminTagSerializer(serializers.ModelSerializer[Tag]):
    class Meta:  # type: ignore
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = ("id", "create_by", "modified_by", "create_at", "modified_at")

    def validate_name(self, value: str) -> str:
        queryset = Tag.objects.filter(name=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("标签名称已存在")
        return value

    def create(self, validated_data: dict[str, object]) -> Tag:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return Tag.objects.create(
            name=validated_data["name"],
            color=validated_data.get("color"),
            create_by=admin_user.id,
            create_at=now,
        )

    def update(self, instance: Tag, validated_data: dict[str, object]) -> Tag:
        admin_user = self.context["admin_user"]
        instance.name = validated_data.get("name", instance.name)
        instance.color = validated_data.get("color", instance.color)
        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save(update_fields=["name", "color", "modified_by", "modified_at"])
        return instance


class AdminPetRanceSerializer(serializers.ModelSerializer[PetRance]):
    class Meta:  # type: ignore
        model = PetRance
        fields = (
            "id",
            "p_id",
            "name",
            "hp",
            "attack",
            "defense",
            "special_attack",
            "special_defense",
            "speed",
            "total",
            "is_delete",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "is_delete",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> PetRance:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return PetRance.objects.create(
            **validated_data,
            is_delete=0,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(self, instance: PetRance, validated_data: dict[str, object]) -> PetRance:
        admin_user = self.context["admin_user"]
        for field in (
            "p_id",
            "name",
            "hp",
            "attack",
            "defense",
            "special_attack",
            "special_defense",
            "speed",
            "total",
        ):
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save()
        return instance


class AdminPetRanceRelationCreateSerializer(serializers.Serializer):
    rance_id = serializers.IntegerField(min_value=1)

    def validate_rance_id(self, value: int) -> int:
        if not PetRance.objects.filter(id=value, is_delete=0).exists():
            raise serializers.ValidationError("种族不存在")
        return value


class AdminPetRanceRelationUpdateSerializer(serializers.Serializer):
    new_rance_id = serializers.IntegerField(min_value=1)

    def validate_new_rance_id(self, value: int) -> int:
        if not PetRance.objects.filter(id=value, is_delete=0).exists():
            raise serializers.ValidationError("种族不存在")
        return value


class AdminPetFeatureSerializer(serializers.ModelSerializer[PetFeature]):
    class Meta:  # type: ignore
        model = PetFeature
        fields = (
            "id",
            "introduction",
            "detail",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> PetFeature:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return PetFeature.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(self, instance: PetFeature, validated_data: dict[str, object]) -> PetFeature:
        admin_user = self.context["admin_user"]
        instance.introduction = validated_data.get(
            "introduction", instance.introduction
        )
        instance.detail = validated_data.get("detail", instance.detail)
        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save(update_fields=["introduction", "detail", "modified_by", "modified_at"])
        return instance


class AdminPetGenerationSerializer(serializers.ModelSerializer[PetGeneration]):
    class Meta:  # type: ignore
        model = PetGeneration
        fields = (
            "id",
            "name",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> PetGeneration:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return PetGeneration.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(
        self, instance: PetGeneration, validated_data: dict[str, object]
    ) -> PetGeneration:
        admin_user = self.context["admin_user"]
        instance.name = validated_data.get("name", instance.name)
        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save(update_fields=["name", "modified_by", "modified_at"])
        return instance


class AdminPetGenerationRelationCreateSerializer(serializers.Serializer):
    generation_id = serializers.IntegerField(min_value=1)

    def validate_generation_id(self, value: int) -> int:
        if not PetGeneration.objects.filter(id=value).exists():
            raise serializers.ValidationError("世代不存在")
        return value


class AdminPetGenerationRelationUpdateSerializer(serializers.Serializer):
    new_generation_id = serializers.IntegerField(min_value=1)

    def validate_new_generation_id(self, value: int) -> int:
        if not PetGeneration.objects.filter(id=value).exists():
            raise serializers.ValidationError("世代不存在")
        return value


class AdminPetSkillSerializer(serializers.ModelSerializer[PetSkill]):
    class Meta:  # type: ignore
        model = PetSkill
        fields = (
            "id",
            "learn_type",
            "category_id",
            "attribute_id",
            "name",
            "introduction",
            "detail",
            "damage",
            "aim",
            "pp",
            "cost_time",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> PetSkill:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return PetSkill.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(self, instance: PetSkill, validated_data: dict[str, object]) -> PetSkill:
        admin_user = self.context["admin_user"]
        for field in (
            "learn_type",
            "category_id",
            "attribute_id",
            "name",
            "introduction",
            "detail",
            "damage",
            "aim",
            "pp",
            "cost_time",
        ):
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save()
        return instance


class AdminItemSerializer(serializers.ModelSerializer[Items]):
    class Meta:  # type: ignore
        model = Items
        fields = (
            "id",
            "name",
            "jp_name",
            "en_name",
            "introduction",
            "detail",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> Items:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return Items.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(self, instance: Items, validated_data: dict[str, object]) -> Items:
        admin_user = self.context["admin_user"]
        for field in ("name", "jp_name", "en_name", "introduction", "detail"):
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save()
        return instance


class AdminPetEggGroupSerializer(serializers.ModelSerializer[PetEggGroup]):
    class Meta:  # type: ignore
        model = PetEggGroup
        fields = (
            "id",
            "name",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> PetEggGroup:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return PetEggGroup.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(self, instance: PetEggGroup, validated_data: dict[str, object]) -> PetEggGroup:
        admin_user = self.context["admin_user"]
        instance.name = validated_data.get("name", instance.name)
        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save(update_fields=["name", "modified_by", "modified_at"])
        return instance


class AdminPetEggGroupRelationCreateSerializer(serializers.Serializer):
    egg_group_id = serializers.IntegerField(min_value=1)

    def validate_egg_group_id(self, value: int) -> int:
        if not PetEggGroup.objects.filter(id=value).exists():
            raise serializers.ValidationError("蛋组不存在")
        return value


class AdminPetEggGroupRelationUpdateSerializer(serializers.Serializer):
    new_egg_group_id = serializers.IntegerField(min_value=1)

    def validate_new_egg_group_id(self, value: int) -> int:
        if not PetEggGroup.objects.filter(id=value).exists():
            raise serializers.ValidationError("蛋组不存在")
        return value


class AdminGameDocsSerializer(serializers.ModelSerializer[GameDocs]):
    class Meta:  # type: ignore
        model = GameDocs
        fields = (
            "id",
            "p_id",
            "name",
            "path",
            "content",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def validate(self, attrs: dict[str, object]) -> dict[str, object]:
        instance = self.instance
        has_parent_id = "p_id" in attrs
        parent_id = attrs.get("p_id", instance.p_id if instance is not None else None)
        if parent_id == 0:
            parent_id = None
            if has_parent_id:
                attrs["p_id"] = None

        if instance is not None and parent_id == instance.id:
            raise serializers.ValidationError("文档不能将自己设为父级")

        if parent_id in (None, ""):
            attrs["content"] = None
            return attrs

        parent = GameDocs.objects.filter(pk=parent_id).first()
        if parent is None:
            raise serializers.ValidationError("文档组不存在")
        if parent.p_id not in (None, 0):
            raise serializers.ValidationError("游戏文档只支持两级结构")

        if instance is not None and GameDocs.objects.filter(p_id=instance.id).exists():
            raise serializers.ValidationError("当前文档组已有子文档，不能再挂到其他组下")

        content = attrs.get("content", instance.content if instance is not None else None)
        if content in (None, ""):
            raise serializers.ValidationError("子文档内容不能为空")

        return attrs

    def create(self, validated_data: dict[str, object]) -> GameDocs:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return GameDocs.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(self, instance: GameDocs, validated_data: dict[str, object]) -> GameDocs:
        admin_user = self.context["admin_user"]
        for field in ("p_id", "name", "path", "content"):
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save()
        return instance


class AdminItemCategorySerializer(serializers.ModelSerializer[ItemCategory]):
    class Meta:  # type: ignore
        model = ItemCategory
        fields = (
            "id",
            "name",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> ItemCategory:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return ItemCategory.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(
        self, instance: ItemCategory, validated_data: dict[str, object]
    ) -> ItemCategory:
        admin_user = self.context["admin_user"]
        instance.name = validated_data.get("name", instance.name)
        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save(update_fields=["name", "modified_by", "modified_at"])
        return instance


class AdminPetSkillCategorySerializer(serializers.ModelSerializer[PetSkillCategory]):
    class Meta:  # type: ignore
        model = PetSkillCategory
        fields = (
            "id",
            "name",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )
        read_only_fields = (
            "id",
            "create_by",
            "modified_by",
            "create_at",
            "modified_at",
        )

    def create(self, validated_data: dict[str, object]) -> PetSkillCategory:
        admin_user = self.context["admin_user"]
        now = timezone.now()
        return PetSkillCategory.objects.create(
            **validated_data,
            create_by=admin_user.id,
            create_at=now,
        )

    def update(
        self, instance: PetSkillCategory, validated_data: dict[str, object]
    ) -> PetSkillCategory:
        admin_user = self.context["admin_user"]
        instance.name = validated_data.get("name", instance.name)
        instance.modified_by = admin_user.id
        instance.modified_at = timezone.now()
        instance.save(update_fields=["name", "modified_by", "modified_at"])
        return instance
