from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source="service.title", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "service",
            "service_title",
            "consumer",
            "provider",
            "status",
            "scheduled_date",
            "scheduled_time",
            "created_at",
        ]
        read_only_fields = ["consumer", "provider", "status", "created_at"]
