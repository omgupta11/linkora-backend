from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.db.models.functions import Power, Sqrt
from .models import Service
from .serializers import ServiceSerializer


# Provider: Create & List own services
class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(provider=self.request.user)

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)


# Consumer: View services by provider
class ProviderServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        provider_id = self.kwargs.get("provider_id")
        return Service.objects.filter(
            provider_id=provider_id,
            is_active=True
        )


# Consumer: Nearby services (radius + filters)
class NearbyServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lat = float(self.request.query_params.get("lat"))
        lng = float(self.request.query_params.get("lng"))
        radius = float(self.request.query_params.get("radius"))

        category = self.request.query_params.get("category")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        qs = Service.objects.filter(is_active=True)

        if category:
            qs = qs.filter(category=category)

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        # distance formula (simple, fast)
        qs = qs.annotate(
            distance=Sqrt(
                Power(F("provider__provider_profile__business_lat") - lat, 2) +
                Power(F("provider__provider_profile__business_lng") - lng, 2)
            ) * 111
        ).filter(distance__lte=radius).order_by("distance")

        return qs
