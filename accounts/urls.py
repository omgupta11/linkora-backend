from django.urls import path
from .views import RegisterAPIView, MeAPIView, EmailTokenView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("me/", MeAPIView.as_view()),
    path("login/", EmailTokenView.as_view()),  # ✅ ONLY LOGIN ENDPOINT
]
