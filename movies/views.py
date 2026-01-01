from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Recommendation
from .serializers import (
    MovieSerializer,
    RecommendationSerializer,
    RecommendationCreateSerializer,
    MovieRecommendationResponseSerializer
)
from .services import TMDBService
from moods.models import Mood
from moods.serializers import MoodSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_movies_view(request):
    """
    Get movie recommendations based on mood
    Fetches 2 movies from TMDB and creates recommendations
    """
    # Handle both JSON and form-encoded data
    data = request.data
    
    # If data is a QueryDict (from form), convert to dict
    if hasattr(data, 'get'):
        data = dict(data)
    
    serializer = RecommendationCreateSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    mood_id = serializer.validated_data['mood_id']
    
    try:
        mood = Mood.objects.get(id=mood_id, is_active=True)
    except Mood.DoesNotExist:
        return Response(
            {'error': 'Mood not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        # Fetch 2 movies from TMDB
        tmdb_movies_data = TMDBService.fetch_movies_by_mood(mood.name, count=2)
        
        if not tmdb_movies_data:
            return Response(
                {'error': 'No movies found for this mood'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create or update Movie objects and Recommendation objects
        movies = []
        recommendation_ids = []
        
        for tmdb_movie in tmdb_movies_data:
            # Create or update movie
            movie = TMDBService.create_or_update_movie(tmdb_movie)
            movies.append(movie)
            
            # Create recommendation (always create new entry)
            recommendation = Recommendation.objects.create(
                user=request.user,
                movie=movie,
                mood=mood,
                recommended_at=timezone.now()
            )
            recommendation_ids.append(recommendation.id)
        
        # Serialize response
        movie_serializer = MovieSerializer(movies, many=True)
        mood_serializer = MoodSerializer(mood)
        
        response_data = {
            'mood': mood_serializer.data,
            'movies': movie_serializer.data,
            'recommendations': recommendation_ids,
            'count': len(movies)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_list_view(request):
    """List all movies in the database"""
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail_view(request, pk):
    """Get movie details by ID"""
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(
            {'error': 'Movie not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = MovieSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation_history_view(request):
    """Get user's recommendation history"""
    recommendations = Recommendation.objects.filter(user=request.user)
    
    # Optional: Filter by mood
    mood_id = request.query_params.get('mood_id')
    if mood_id:
        recommendations = recommendations.filter(mood_id=mood_id)
    
    serializer = RecommendationSerializer(recommendations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendation_detail_view(request, pk):
    """Get specific recommendation details"""
    try:
        recommendation = Recommendation.objects.get(pk=pk, user=request.user)
    except Recommendation.DoesNotExist:
        return Response(
            {'error': 'Recommendation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = RecommendationSerializer(recommendation)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_recommendation_viewed_view(request, pk):
    """Mark a recommendation as viewed"""
    try:
        recommendation = Recommendation.objects.get(pk=pk, user=request.user)
    except Recommendation.DoesNotExist:
        return Response(
            {'error': 'Recommendation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    recommendation.viewed = True
    recommendation.save()
    
    serializer = RecommendationSerializer(recommendation)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_recommendation_view(request, pk):
    """Delete a recommendation from history"""
    try:
        recommendation = Recommendation.objects.get(pk=pk, user=request.user)
    except Recommendation.DoesNotExist:
        return Response(
            {'error': 'Recommendation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    recommendation.delete()
    return Response(
        {'message': 'Recommendation deleted successfully'},
        status=status.HTTP_200_OK
    )


# Template Views for HTML frontend
@login_required
def mood_selection_template_view(request):
    """Template view for mood selection"""
    moods = Mood.objects.filter(is_active=True)
    return render(request, 'movies/mood_selection.html', {'moods': moods})


@login_required
def get_recommendations_template_view(request, mood_id):
    """Template view to get recommendations and display movies"""
    mood = get_object_or_404(Mood, id=mood_id, is_active=True)
    
    try:
        # Fetch 2 movies from TMDB
        tmdb_movies_data = TMDBService.fetch_movies_by_mood(mood.name, count=2)
        
        if not tmdb_movies_data:
            messages.error(request, 'No movies found for this mood. Please try again.')
            return redirect('movies:mood-selection')
        
        # Create or update Movie objects and Recommendation objects
        movies = []
        
        for tmdb_movie in tmdb_movies_data:
            # Create or update movie
            movie = TMDBService.create_or_update_movie(tmdb_movie)
            movies.append(movie)
            
            # Create recommendation (always create new entry)
            Recommendation.objects.create(
                user=request.user,
                movie=movie,
                mood=mood,
                recommended_at=timezone.now()
            )
        
        messages.success(request, f'Found {len(movies)} movies for {mood.name} mood!')
        return render(request, 'movies/movie_list.html', {'movies': movies, 'mood': mood})
        
    except Exception as e:
        messages.error(request, f'Error fetching movies: {str(e)}')
        return redirect('movies:mood-selection')


@login_required
def recommendation_history_template_view(request):
    """Template view for recommendation history"""
    recommendations = Recommendation.objects.filter(user=request.user).order_by('-recommended_at')
    return render(request, 'movies/recommendation_history.html', {'recommendations': recommendations})
