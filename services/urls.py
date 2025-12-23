from django.urls import path
from .views import (
    ServiceListCreateView,
    ServiceRadiusListView,
)

urlpatterns = [
    # provider
    path("", ServiceListCreateView.as_view()),

    # consumer (radius based)
    path("nearby/", ServiceRadiusListView.as_view()),
]
