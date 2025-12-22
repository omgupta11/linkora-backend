from django.urls import path
from .views import ServiceListCreateView, ProviderServiceListView

urlpatterns = [
    path("", ServiceListCreateView.as_view()),
    path("provider/<int:provider_id>/", ProviderServiceListView.as_view()),
]
