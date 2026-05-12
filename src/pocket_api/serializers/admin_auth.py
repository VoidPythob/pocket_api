from __future__ import annotations

from django.utils import timezone
from rest_framework import serializers

from pocket_api.models import AdminUser


class AdminRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        trim_whitespace=False,
    )
    password_confirm = serializers.CharField(
        max_length=128,
        write_only=True,
        trim_whitespace=False,
    )

    def validate_email(self, value: str) -> str:
        if AdminUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("passwords do not match")
        return attrs

    def create(self, validated_data: dict[str, str]) -> AdminUser:
        validated_data.pop("password_confirm")
        return AdminUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            create_at=timezone.now(),
        )
