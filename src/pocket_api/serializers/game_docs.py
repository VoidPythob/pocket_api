from rest_framework import serializers


class GameDocsQuerySerializer(serializers.Serializer):
    group_id = serializers.IntegerField(min_value=1, required=False)


class GameDocListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    p_id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
    path = serializers.CharField(allow_null=True)


class GameDocDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    p_id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
    path = serializers.CharField(allow_null=True)
    content = serializers.CharField(allow_null=True)


class GameDocCategoryChildSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    p_id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
    path = serializers.CharField(allow_null=True)


class GameDocCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    p_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    path = serializers.CharField(allow_null=True)
    children = GameDocCategoryChildSerializer(many=True)
