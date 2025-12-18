from rest_framework import generics, permissions
from .models import Booking
from .serializers import BookingSerializer
from services.models import Service


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "consumer":
            raise PermissionError("Only consumers can book services")

        service = Service.objects.get(id=self.request.data.get("service"))
        serializer.save(
            consumer=user,
            provider=service.provider,
            service=service
        )


class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "consumer":
            return Booking.objects.filter(consumer=user)
        return Booking.objects.filter(provider=user)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class BookingStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        user = request.user
        new_status = request.data.get("status")

        # allowed statuses
        allowed_statuses = ["accepted", "completed", "cancelled"]
        if new_status not in allowed_statuses:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Provider rules
        if user.role == "provider" and booking.provider != user:
            return Response({"error": "Not your booking"}, status=403)

        # Consumer rules
        if user.role == "consumer" and booking.consumer != user:
            return Response({"error": "Not your booking"}, status=403)

        booking.status = new_status
        booking.save()

        return Response(
            {"message": f"Booking marked as {new_status}"},
            status=status.HTTP_200_OK
        )
from django.urls import path
from .views import BookingCreateView, MyBookingsView, BookingStatusUpdateView

urlpatterns = [
    path("", BookingCreateView.as_view(), name="booking-create"),
    path("my/", MyBookingsView.as_view(), name="my-bookings"),
    path("<int:booking_id>/status/", BookingStatusUpdateView.as_view(), name="booking-status"),
]
