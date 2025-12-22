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

        # attach profile data depending on role
        if user.role == User.Roles.CONSUMER and hasattr(user, "consumer_profile"):
            data["consumer_profile"] = ConsumerProfileSerializer(
                user.consumer_profile
            ).data

        elif user.role == User.Roles.PROVIDER and hasattr(user, "provider_profile"):
            data["provider_profile"] = ProviderProfileSerializer(
                user.provider_profile
            ).data

        return Response(data)

    def put(self, request):
        user = request.user

        # update basic user fields
        for field in ("username", "email", "phone", "avatar"):
            if field in request.data:
                setattr(user, field, request.data[field])

        user.save()

        # update profile
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

        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
