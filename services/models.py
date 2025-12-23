from django.db import models
from django.conf import settings

class Service(models.Model):
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="services"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)

    duration_minutes = models.PositiveIntegerField()

    # location (provider based)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
