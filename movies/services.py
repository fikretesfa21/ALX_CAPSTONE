import requests
from django.conf import settings
from .models import Movie


class TMDBService:
    """Service class for interacting with TMDB API"""
    
    BASE_URL = 'https://api.themoviedb.org/3'
    
    # Mood to Genre ID mapping
    MOOD_GENRE_MAP = {
        'Happy': [35, 16],  # Comedy, Animation
        'Sad': [18, 10749],  # Drama, Romance
        'Excited': [28, 12, 53],  # Action, Adventure, Thriller
        'Relaxed': [18, 99, 10751],  # Drama, Documentary, Family
        'Romantic': [10749, 18],  # Romance, Drama
    }
    
    @classmethod
    def _get_api_key(cls):
        """Get TMDB API key from settings"""
        api_key = getattr(settings, 'TMDB_API_KEY', '')
        if not api_key:
            raise ValueError('TMDB_API_KEY not configured in settings')
        return api_key
    
    @classmethod
    def _make_request(cls, endpoint, params=None):
        """Make a request to TMDB API"""
        api_key = cls._get_api_key()
        url = f"{cls.BASE_URL}{endpoint}"
        
        if params is None:
            params = {}
        params['api_key'] = api_key
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"TMDB API request failed: {str(e)}")
    
    @classmethod
    def get_genres_for_mood(cls, mood_name):
        """Get genre IDs for a given mood"""
        return cls.MOOD_GENRE_MAP.get(mood_name, [18])  # Default to Drama if mood not found
    
    @classmethod
    def fetch_movies_by_mood(cls, mood_name, count=2):
        """
        Fetch movies from TMDB based on mood
        Returns list of movie data dictionaries
        """
        genre_ids = cls.get_genres_for_mood(mood_name)
        
        # Use the first genre for the query (TMDB allows multiple genres with '|')
        # For simplicity, we'll use the first genre
        primary_genre = genre_ids[0] if genre_ids else 18
        
        params = {
            'with_genres': primary_genre,
            'sort_by': 'popularity.desc',
            'page': 1,
        }
        
        try:
            response_data = cls._make_request('/discover/movie', params)
            movies = response_data.get('results', [])
            
            # Limit to requested count (2 movies)
            return movies[:count]
        except Exception as e:
            raise Exception(f"Failed to fetch movies: {str(e)}")
    
    @classmethod
    def create_or_update_movie(cls, tmdb_movie_data):
        """
        Create or update a Movie object from TMDB API data
        Returns the Movie instance
        """
        tmdb_id = tmdb_movie_data.get('id')
        if not tmdb_id:
            raise ValueError('Movie data must include id')
        
        # Build poster URL
        poster_path = tmdb_movie_data.get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        
        # Build backdrop URL
        backdrop_path = tmdb_movie_data.get('backdrop_path', '')
        backdrop_url = f"https://image.tmdb.org/t/p/w1280{backdrop_path}" if backdrop_path else None
        
        # Parse release date
        release_date = tmdb_movie_data.get('release_date')
        if release_date:
            try:
                from datetime import datetime
                release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                release_date = None
        else:
            release_date = None
        
        movie, created = Movie.objects.update_or_create(
            tmdb_id=tmdb_id,
            defaults={
                'title': tmdb_movie_data.get('title', ''),
                'overview': tmdb_movie_data.get('overview', ''),
                'release_date': release_date,
                'poster_url': poster_url,
                'backdrop_url': backdrop_url,
                'rating': tmdb_movie_data.get('vote_average'),
                'genre_ids': tmdb_movie_data.get('genre_ids', []),
                'external_api_data': tmdb_movie_data,
            }
        )
        
        return movie

