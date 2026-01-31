from rest_framework import serializers
from .models import User, ConsumerProfile, ProviderProfile


class ConsumerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerProfile
        exclude = ("id", "user")


class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        exclude = ("id", "user")


class UserSerializer(serializers.ModelSerializer):
    consumer_profile = ConsumerProfileSerializer(read_only=True)
    provider_profile = ProviderProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "role",
            "phone",
            "is_verified",
            "consumer_profile",
            "provider_profile",
        )
