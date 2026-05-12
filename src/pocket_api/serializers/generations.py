from rest_framework import serializers


class GenerationPayloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(allow_null=True)
