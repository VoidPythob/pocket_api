from rest_framework import serializers


class ItemListQuerySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(min_value=1, required=False)
    name = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def validate_name(self, value: str) -> str:
        return value.strip()


class ItemCategoryPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)


class ItemPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    jp_name = serializers.CharField(allow_null=True)
    en_name = serializers.CharField(allow_null=True)
    introduction = serializers.CharField(allow_null=True)
    detail = serializers.CharField(allow_null=True)
    categories = ItemCategoryPayloadSerializer(many=True)
