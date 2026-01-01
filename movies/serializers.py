from rest_framework import serializers
from .models import Movie, Recommendation
from moods.serializers import MoodSerializer
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model"""
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'overview', 'release_date', 
            'poster_url', 'backdrop_url', 'rating', 
            'tmdb_id', 'created_at'
        ]
        read_only_fields = fields


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model"""
    movie = MovieSerializer(read_only=True)
    mood = MoodSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'user', 'movie', 'mood', 
            'recommended_at', 'viewed', 'user_rating'
        ]
        read_only_fields = ['id', 'user', 'recommended_at']


class RecommendationCreateSerializer(serializers.Serializer):
    """Serializer for creating recommendations"""
    mood_id = serializers.IntegerField()
    
    def validate_mood_id(self, value):
        from moods.models import Mood
        try:
            mood = Mood.objects.get(id=value, is_active=True)
        except Mood.DoesNotExist:
            raise serializers.ValidationError('Invalid mood ID')
        return value


class MovieRecommendationResponseSerializer(serializers.Serializer):
    """Serializer for recommendation response"""
    mood = MoodSerializer()
    movies = MovieSerializer(many=True)
    recommendations = serializers.ListField(
        child=serializers.IntegerField(),
        read_only=True
    )
    count = serializers.IntegerField()

