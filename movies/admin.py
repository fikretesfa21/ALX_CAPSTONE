from django.contrib import admin
from .models import Movie, Recommendation


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'rating', 'tmdb_id', 'created_at']
    list_filter = ['created_at', 'release_date']
    search_fields = ['title', 'overview']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'mood', 'recommended_at', 'viewed', 'user_rating']
    list_filter = ['mood', 'viewed', 'recommended_at']
    search_fields = ['user__username', 'movie__title']
    readonly_fields = ['recommended_at']
