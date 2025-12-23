from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ConsumerProfileSerializer,
    ProviderProfileSerializer,
)

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data

        if user.role == User.Roles.CONSUMER:
            data["consumer_profile"] = ConsumerProfileSerializer(
                user.consumer_profile
            ).data
        else:
            data["provider_profile"] = ProviderProfileSerializer(
                user.provider_profile
            ).data

        return Response(data)

    def put(self, request):
        user = request.user

        for field in ("username", "email", "phone", "avatar"):
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()

        if user.role == User.Roles.CONSUMER:
            serializer = ConsumerProfileSerializer(
                user.consumer_profile,
                data=request.data.get("consumer_profile", {}),
                partial=True,
            )
        else:
            serializer = ProviderProfileSerializer(
                user.provider_profile,
                data=request.data.get("provider_profile", {}),
                partial=True,
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(user).data)


class UpdateLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role == User.Roles.CONSUMER:
            serializer = ConsumerProfileSerializer(
                user.consumer_profile,
                data=request.data,
                partial=True,
            )
        else:
            serializer = ProviderProfileSerializer(
                user.provider_profile,
                data=request.data,
                partial=True,
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
