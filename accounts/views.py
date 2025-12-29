from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import get_user_model

from .models import ConsumerProfile, ProviderProfile
from .serializers import UserSerializer

User = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        # ------------------------
        # CREATE USER
        # ------------------------
        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
            phone=data.get("phone"),
        )

        # ------------------------
        # CONSUMER PROFILE
        # ------------------------
        if user.role == "consumer":
            ConsumerProfile.objects.create(
                user=user,
                full_name=data["full_name"],
                dob=data.get("dob"),
                address=data["address"],
                city=data["city"],
                state=data["state"],
                country=data.get("country", "India"),
                pincode=data["pincode"],
                profile_image=data.get("profile_image"),
            )

        # ------------------------
        # PROVIDER PROFILE
        # ------------------------
        if user.role == "provider":
            ProviderProfile.objects.create(
                user=user,
                business_name=data["business_name"],
                owner_name=data["owner_name"],
                category=data["category"],
                address=data["address"],
                city=data["city"],
                state=data["state"],
                country=data.get("country", "India"),
                pincode=data["pincode"],
                landmark=data.get("landmark", ""),
                gst_number=data.get("gst_number", ""),
                cover_image=data.get("cover_image"),
            )

        return Response(
            {"message": "Account created successfully"},
            status=status.HTTP_201_CREATED,
        )


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
