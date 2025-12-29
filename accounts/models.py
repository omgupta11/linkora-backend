from django.db import models
from django.contrib.auth.models import AbstractUser

# ----------------------
# USER MODEL
# ----------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ("consumer", "Consumer"),
        ("provider", "Provider"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="consumer",
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    # 🔥 FIX: this was causing NOT NULL crash
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# ----------------------
# CONSUMER PROFILE
# ----------------------
class ConsumerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="consumer_profile",
    )

    full_name = models.CharField(max_length=200)

    dob = models.DateField(
        null=True,
        blank=True,
    )

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=10)

    profile_image = models.ImageField(
        upload_to="consumers/",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


# ----------------------
# PROVIDER PROFILE
# ----------------------
class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider_profile",
    )

    business_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)

    category = models.CharField(max_length=100)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    pincode = models.CharField(max_length=10)

    landmark = models.CharField(
        max_length=200,
        blank=True,
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True,
    )

    cover_image = models.ImageField(
        upload_to="providers/",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
