from django.db import models
from django.contrib.auth.models import User
from moods.models import Mood


class Movie(models.Model):
    """Movie model to store movie data from TMDB API"""
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateField(blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)
    backdrop_url = models.URLField(blank=True, null=True)
    tmdb_id = models.IntegerField(unique=True)
    rating = models.FloatField(blank=True, null=True)
    genre_ids = models.JSONField(default=list, blank=True)
    external_api_data = models.JSONField(default=dict, blank=True)  # Store full API response
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Recommendation(models.Model):
    """Recommendation model linking User, Movie, and Mood"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='recommendations')
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='recommendations')
    recommended_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    user_rating = models.IntegerField(blank=True, null=True)  # Optional: user rating 1-5

    class Meta:
        ordering = ['-recommended_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.mood.name})"
