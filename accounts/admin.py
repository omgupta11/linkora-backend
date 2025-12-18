from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, ConsumerProfile, ProviderProfile

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Extra', {'fields': ('role','phone','avatar','is_verified','points','level')}),
    )

admin.site.register(ConsumerProfile)
admin.site.register(ProviderProfile)
