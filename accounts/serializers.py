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
    consumer_profile = ConsumerProfileSerializer(required=False)
    provider_profile = ProviderProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "phone",
            "is_verified",
            "consumer_profile",
            "provider_profile",
        )
