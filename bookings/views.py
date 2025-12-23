from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Booking
from .serializers import BookingSerializer
from services.models import Service


# -------------------------------------------------
# Consumer: Create booking
# -------------------------------------------------
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "consumer":
            raise permissions.PermissionDenied(
                "Only consumers can book services"
            )

        service = get_object_or_404(
            Service,
            id=self.request.data.get("service")
        )

        # 🔴 SLOT CONFLICT CHECK (THIS IS WHAT YOU ASKED)
        exists = Booking.objects.filter(
            service=service,
            scheduled_date=self.request.data.get("scheduled_date"),
            scheduled_time=self.request.data.get("scheduled_time"),
            status__in=["pending", "accepted"]
        ).exists()

        if exists:
            raise ValidationError("This slot is already booked")

        # ✅ CREATE BOOKING
        serializer.save(
            consumer=user,
            provider=service.provider,
            service=service
        )


# -------------------------------------------------
# Consumer & Provider: View own bookings
# -------------------------------------------------
class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "consumer":
            return Booking.objects.filter(consumer=user)

        return Booking.objects.filter(provider=user)


# -------------------------------------------------
# Update booking status
# -------------------------------------------------
class BookingStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        user = request.user
        new_status = request.data.get("status")

        allowed_statuses = ["accepted", "completed", "cancelled"]
        if new_status not in allowed_statuses:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Provider rules
        if user.role == "provider" and booking.provider != user:
            return Response(
                {"error": "Not your booking"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Consumer rules
        if user.role == "consumer" and booking.consumer != user:
            return Response(
                {"error": "Not your booking"},
                status=status.HTTP_403_FORBIDDEN
            )

        booking.status = new_status
        booking.save()

        return Response(
            {"message": f"Booking marked as {new_status}"},
            status=status.HTTP_200_OK
        )
