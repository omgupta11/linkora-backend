from django.urls import path
from .views import RegisterAPIView, MeAPIView, UpdateLocationAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("me/", MeAPIView.as_view()),
    path("location/", UpdateLocationAPIView.as_view()),
]
