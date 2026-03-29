from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    farm = models.ForeignKey('farms.Farm', on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    farmer_response = models.TextField(blank=True)
    farmer_responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['farm', 'author']

    def __str__(self):
        return f"{self.author.username} - {self.farm.name} ({self.rating}/5)"

    @property
    def star_display(self):
        return '★' * self.rating + '☆' * (5 - self.rating)
