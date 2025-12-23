from django.urls import path
from .views import RegisterAPIView, MeAPIView, UpdateLocationAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("location/", UpdateLocationAPIView.as_view(), name="location"),
]
