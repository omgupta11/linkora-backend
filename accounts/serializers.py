from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ConsumerProfile, ProviderProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "role",
            "phone",
            "avatar",
            "is_verified",
            "points",
            "level",
        )
        read_only_fields = ("id", "is_verified", "points", "level")


class ConsumerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerProfile
        fields = (
            "permanent_address",
            "current_lat",
            "current_lng",
            "bio",
        )


class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = (
            "business_name",
            "business_address",
            "business_city",
            "business_category",
            "business_phone",
            "business_logo",
            "working_hours",
            "about",
            "business_lat",
            "business_lng",
            "average_rating",
            "total_reviews",
        )
        read_only_fields = ("average_rating", "total_reviews")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=User.Roles.choices)

    consumer_profile = ConsumerProfileSerializer(required=False)
    provider_profile = ProviderProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "role",
            "phone",
            "avatar",
            "consumer_profile",
            "provider_profile",
        )

    def create(self, validated_data):
        consumer_data = validated_data.pop("consumer_profile", None)
        provider_data = validated_data.pop("provider_profile", None)
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if user.role == User.Roles.CONSUMER and consumer_data:
            ConsumerProfile.objects.filter(user=user).update(**consumer_data)

        if user.role == User.Roles.PROVIDER and provider_data:
            ProviderProfile.objects.filter(user=user).update(**provider_data)

        return user
