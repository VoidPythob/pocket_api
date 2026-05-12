from rest_framework import serializers


class AdminFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class FileUploadPayloadSerializer(serializers.Serializer):
    file_id = serializers.CharField()
    file_name = serializers.CharField()
    content_type = serializers.CharField(allow_null=True)
    size = serializers.IntegerField()
    url = serializers.CharField()
