from rest_framework import serializers

from pocket_api.models import Pets


class PetListQuerySerializer(serializers.Serializer):
    generation_id = serializers.IntegerField(min_value=1, required=True)
    feature_id = serializers.IntegerField(min_value=1, required=False)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def validate_name(self, value: str) -> str:
        return value.strip()


class PetFeatureListQuerySerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def validate_name(self, value: str) -> str:
        return value.strip()


class PetTagPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
    color = serializers.CharField(allow_null=True)


class PetFeaturePayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    introduction = serializers.CharField(allow_null=True)
    detail = serializers.CharField(allow_null=True)


class PetEggGroupPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)


class PetRancePayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
    hp = serializers.IntegerField(allow_null=True)
    attack = serializers.IntegerField(allow_null=True)
    defense = serializers.IntegerField(allow_null=True)
    special_attack = serializers.IntegerField(allow_null=True)
    special_defense = serializers.IntegerField(allow_null=True)
    speed = serializers.IntegerField(allow_null=True)
    total = serializers.IntegerField(allow_null=True)


class PetSkillPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    learn_type = serializers.IntegerField(allow_null=True)
    category_id = serializers.IntegerField(allow_null=True)
    attribute_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    introduction = serializers.CharField(allow_null=True)
    detail = serializers.CharField(allow_null=True)
    damage = serializers.IntegerField(allow_null=True)
    aim = serializers.IntegerField(allow_null=True)
    pp = serializers.IntegerField(allow_null=True)
    cost_time = serializers.IntegerField(allow_null=True)


class PetImagePayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_url = serializers.CharField()
    sort = serializers.IntegerField()
    is_cover = serializers.IntegerField()


class PetCaptureMethodPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    pet_region_id = serializers.IntegerField(allow_null=True)
    region_name = serializers.CharField(allow_null=True)
    method = serializers.CharField(allow_null=True)
    detail = serializers.CharField(allow_null=True)


class PetListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    jp_name = serializers.CharField()
    en_name = serializers.CharField()
    first_image_url = serializers.CharField(allow_null=True)
    tags = PetTagPayloadSerializer(many=True)
    features = PetFeaturePayloadSerializer(many=True)


class PetDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    jp_name = serializers.CharField()
    en_name = serializers.CharField()
    weight = serializers.IntegerField()
    gender_male_ratio = serializers.IntegerField(allow_null=True)
    gender_ratio_display = serializers.CharField(allow_null=True)
    base_point_type = serializers.IntegerField(allow_null=True)
    base_point_value = serializers.IntegerField(allow_null=True)
    capture_probability = serializers.IntegerField(allow_null=True)
    egg_hatching_steps = serializers.IntegerField(allow_null=True)
    first_image_url = serializers.CharField(allow_null=True)
    images = PetImagePayloadSerializer(many=True)
    tags = PetTagPayloadSerializer(many=True)
    egg_groups = PetEggGroupPayloadSerializer(many=True)
    features = PetFeaturePayloadSerializer(many=True)
    rances = PetRancePayloadSerializer(many=True)
    skills = PetSkillPayloadSerializer(many=True)
    create_by = serializers.IntegerField()
    modified_by = serializers.IntegerField(allow_null=True)
    create_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField(allow_null=True)


class PetsSerializer(serializers.ModelSerializer[Pets]):
    class Meta:  # type: ignore
        model = Pets
        fields = "__all__"
