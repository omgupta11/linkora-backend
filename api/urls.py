from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # --------------------
    # ADMIN
    # --------------------
    path("admin/", admin.site.urls),

    # --------------------
    # AUTH (JWT)
    # --------------------
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/", include("accounts.urls")),

    # --------------------
    # APP MODULES
    # --------------------
    path("api/services/", include("services.urls")),
    path("api/bookings/", include("bookings.urls")),
    path("api/reviews/", include("reviews_app.urls")),
    path("api/notifications/", include("notifications_app.urls")),
]

# --------------------
# MEDIA (IMAGE UPLOADS)
# --------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
