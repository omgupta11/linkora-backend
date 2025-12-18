from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source="provider.username", read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "provider",
            "provider_name",
            "title",
            "description",
            "price",
            "category",
            "duration_minutes",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["provider", "created_at"]
