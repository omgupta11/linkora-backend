from math import radians, cos, sin, asin, sqrt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Service
from .serializers import ServiceSerializer


# 🔢 Haversine distance calculation (KM)
def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(
        radians, [lon1, lat1, lon2, lat2]
    )
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c  # KM


# ✅ PROVIDER: Create & list own services
class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(provider=self.request.user)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


# ✅ CONSUMER: Radius‑based service listing
class ServiceRadiusListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            lat = float(self.request.query_params.get("lat"))
            lng = float(self.request.query_params.get("lng"))
            radius = float(self.request.query_params.get("radius"))
        except (TypeError, ValueError):
            raise ValidationError("lat, lng, radius are required")

        services = Service.objects.filter(
            is_active=True,
            lat__isnull=False,
            lng__isnull=False
        )

        result = []
        for service in services:
            distance = haversine(
                lat, lng,
                float(service.lat),
                float(service.lng)
            )
            if distance <= radius:
                result.append(service.id)

        return Service.objects.filter(id__in=result)
