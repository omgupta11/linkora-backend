from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ConsumerProfile, ProviderProfile
from .serializers import UserSerializer

User = get_user_model()

# -----------------------------
# JWT LOGIN WITH EMAIL
# -----------------------------
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        attrs["username"] = attrs.get("email")
        return super().validate(attrs)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


# -----------------------------
# REGISTER
# -----------------------------
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        if User.objects.filter(email=data["email"]).exists():
            return Response(
                {"email": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
            role=data["role"],
            phone=data.get("phone"),
        )

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


# -----------------------------
# ME
# -----------------------------
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
