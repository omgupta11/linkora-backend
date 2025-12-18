from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # JWT Auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Accounts
    path("api/accounts/", include("accounts.urls")),

    # Services
    path("api/services/", include("services.urls")),

    # Bookings
    path("api/bookings/", include("bookings.urls")),

    # Reviews
    path("api/reviews/", include("reviews_app.urls")),

    path("api/notifications/", include("notifications_app.urls")),

]
