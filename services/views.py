from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
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
