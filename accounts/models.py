from django.db import models
from django.contrib.auth.models import AbstractUser


# ============================
# CUSTOM USER MODEL (EMAIL LOGIN)
# ============================
class User(AbstractUser):
    # 🔑 Use email for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # username still required internally

    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("consumer", "Consumer"),
        ("provider", "Provider"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="consumer",
    )

    phone = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# ============================
# CONSUMER PROFILE
# ============================
class ConsumerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="consumer_profile",
    )

    full_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=10)
    profile_image = models.ImageField(upload_to="consumers/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# ============================
# PROVIDER PROFILE
# ============================
class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider_profile",
    )

    business_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=10, blank=True, null=True)
    landmark = models.CharField(max_length=200, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    cover_image = models.ImageField(upload_to="providers/covers/", blank=True, null=True)
    owner_image = models.ImageField(upload_to="providers/owners/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
