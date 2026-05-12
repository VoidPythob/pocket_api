from __future__ import annotations

from rest_framework import serializers


class AdminPokemonCsvImportSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    overwrite_existing = serializers.BooleanField(required=False, default=True)

    def validate_file(self, value):
        file_name = getattr(value, "name", "")
        if file_name and not file_name.lower().endswith(".csv"):
            raise serializers.ValidationError("only csv files are supported")
        return value
