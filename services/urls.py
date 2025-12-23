from django.urls import path
from .views import (
    ServiceListCreateView,
    ProviderServiceListView,
    NearbyServiceListView,
)

urlpatterns = [
    path("", ServiceListCreateView.as_view()),
    path("provider/<int:provider_id>/", ProviderServiceListView.as_view()),
    path("nearby/", NearbyServiceListView.as_view()),
]
