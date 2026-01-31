from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConsumerProfile, ProviderProfile
from .serializers import UserSerializer

User = get_user_model()


# ============================
# REGISTER (CONSUMER / PROVIDER)
# ============================
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)  # 🔥 REQUIRED FOR FORM + IMAGES

    def post(self, request):
        data = request.data

        # ---- basic validation ----

        # ---- basic validation ----
        required_fields = ["email", "password", "role"]
        for field in required_fields:
            if not data.get(field):
                return Response({field: "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=data.get("email")).exists():
            return Response(
                {"email": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ---- provider validation ----
        if data.get("role") == "provider":
            provider_fields = ["business_name", "owner_name", "category"]
            for field in provider_fields:
                if not data.get(field):
                    return Response({field: "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

        # ---- create user ----
        try:
            user = User.objects.create_user(
                username=data["email"],        # EMAIL == USERNAME
                email=data["email"],
                password=data["password"],
                role=data["role"],
                phone=data.get("phone"),
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # ---- consumer profile ----
        try:
            if user.role == "consumer":
                ConsumerProfile.objects.create(
                    user=user,
                    full_name=data["full_name"],
                    address=data.get("address", ""),
                    city=data.get("city", ""),
                    state=data.get("state", ""),
                    country=data.get("country", "India"),
                    pincode=data.get("pincode", ""),
                    profile_image=data.get("profile_image"),
                )

            # ---- provider profile ----
            if user.role == "provider":
                ProviderProfile.objects.create(
                    user=user,
                    business_name=data["business_name"],
                    owner_name=data["owner_name"],
                    category=data["category"],
                    address=data.get("address", ""),
                    city=data.get("city", ""),
                    state=data.get("state", ""),
                    country=data.get("country", "India"),
                    pincode=data.get("pincode", ""),
                    landmark=data.get("landmark", ""),
                    gst_number=data.get("gst_number"),
                    cover_image=data.get("cover_image"),
                    owner_image=data.get("owner_image"),
                )
        except Exception as e:
            user.delete() # cleanup
            return Response({"error": f"Profile creation failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Account created successfully"},
            status=status.HTTP_201_CREATED,
        )


# ============================
# ME (PROFILE)
# ============================
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ============================
# EMAIL LOGIN (MANUAL JWT)
# ============================
class EmailTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            }
        })
