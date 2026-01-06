from django.urls import path
from .views import RegisterAPIView, MeAPIView, EmailTokenObtainPairView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("token/", EmailTokenObtainPairView.as_view(), name="token"),
]

