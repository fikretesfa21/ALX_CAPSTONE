from django.db import models


class Mood(models.Model):
    """Mood model for movie recommendations"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
