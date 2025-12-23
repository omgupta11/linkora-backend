from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Roles(models.TextChoices):
        CONSUMER = "consumer", _("Consumer")
        PROVIDER = "provider", _("Provider")

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CONSUMER
    )

    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    # flags
    is_verified = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    level = models.CharField(max_length=32, default="Bronze")

    def __str__(self):
        return f"{self.username} ({self.role})"


class ConsumerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="consumer_profile"
    )

    permanent_address = models.TextField(blank=True)

    current_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    current_lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return f"ConsumerProfile: {self.user.username}"


class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )

    business_name = models.CharField(max_length=255, blank=True)
    business_address = models.TextField(blank=True)
    business_city = models.CharField(max_length=128, blank=True)
    business_category = models.CharField(max_length=128, blank=True)
    business_phone = models.CharField(max_length=20, blank=True)
    business_logo = models.URLField(blank=True, null=True)
    working_hours = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0
    )
    total_reviews = models.IntegerField(default=0)

    def __str__(self):
        return f"ProviderProfile: {self.business_name or self.user.username}"


# -------------------------------------------------
# SIGNALS
# -------------------------------------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == User.Roles.CONSUMER:
        ConsumerProfile.objects.create(user=instance)

    elif instance.role == User.Roles.PROVIDER:
        ProviderProfile.objects.create(user=instance)
