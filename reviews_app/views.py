from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Review
from .serializers import ReviewSerializer
from bookings.models import Booking


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = Booking.objects.get(id=self.request.data.get("booking"))
        user = self.request.user

        if user.role != "consumer":
            raise ValidationError("Only consumers can leave reviews")

        if booking.consumer != user:
            raise ValidationError("Not your booking")

        if booking.status != "completed":
            raise ValidationError("Booking not completed yet")

        if hasattr(booking, "review"):
            raise ValidationError("Review already exists")

        serializer.save(
            booking=booking,
            consumer=user,
            provider=booking.provider
        )
