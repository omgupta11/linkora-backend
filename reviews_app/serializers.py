from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    consumer_name = serializers.CharField(
        source="consumer.username",
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "booking",
            "consumer_name",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["created_at"]
