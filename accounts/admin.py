from django.contrib import admin
from .models import User, ConsumerProfile, ProviderProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_verified", "is_staff")
    list_filter = ("role", "is_verified")
    search_fields = ("username", "email")


@admin.register(ConsumerProfile)
class ConsumerProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "city", "state", "country", "created_at")
    search_fields = ("full_name", "city", "state")


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("business_name", "owner_name", "city", "state", "created_at")
    search_fields = ("business_name", "owner_name", "city")
