from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    is_farmer = models.BooleanField(default=False)
    default_latitude = models.FloatField(null=True, blank=True)
    default_longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.display_name or self.user.username
