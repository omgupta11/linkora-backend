from django.urls import path
from .views import (
    BookingCreateView,
    MyBookingsView,
    BookingStatusUpdateView,
)

urlpatterns = [
    path("", BookingCreateView.as_view(), name="booking-create"),
    path("my/", MyBookingsView.as_view(), name="my-bookings"),
    path(
        "<int:booking_id>/status/",
        BookingStatusUpdateView.as_view(),
        name="booking-status",
    ),
]
