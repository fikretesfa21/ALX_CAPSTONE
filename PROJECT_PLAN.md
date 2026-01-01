# Movieflick - Movie Recommendation Platform

## Project Plan & Architecture

### Overview

A Django-based REST API platform for mood-based movie recommendations with user authentication and recommendation history.

---

## 1. Project Structure

```
movieflick/
├── movieflick/              # Main Django project directory
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # User authentication app
│   ├── models.py
│   ├── views.py             # API views + template views
│   ├── serializers.py
│   ├── urls.py
│   ├── permissions.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           └── register.html
├── movies/                  # Movie recommendations app (main app)
│   ├── models.py
│   ├── views.py             # API views + template views
│   ├── serializers.py
│   ├── urls.py
│   ├── services.py          # External API integration
│   ├── utils.py
│   └── templates/
│       └── movies/
│           ├── mood_selection.html
│           ├── movie_list.html
│           └── recommendation_history.html
├── moods/                   # Mood management app
│   ├── models.py
│   ├── serializers.py
│   └── urls.py
├── templates/               # Base templates
│   └── base.html
├── static/                  # CSS and static files
│   └── css/
│       └── style.css
├── requirements.txt
├── .env                     # Environment variables (API keys)
├── manage.py
└── README.md
```

---

## 2. Django Apps & Responsibilities

### 2.1 Accounts App

- **Purpose**: User authentication and management
- **Models**: Custom User model (extends AbstractUser) or use default User
- **Features**: Registration, Login, Logout, User Profile

### 2.2 Movies App (Core App)

- **Purpose**: Movie recommendations, fetching, and storage
- **Models**: Movie, Recommendation, UserMovieHistory
- **Features**:
  - External API integration (TMDB, OMDB, or similar)
  - Movie fetching based on moods
  - Recommendation history management

### 2.3 Moods App (Optional but Recommended)

- **Purpose**: Manage mood definitions
- **Models**: Mood
- **Features**: CRUD operations for moods
- **Default Moods**: Happy, Sad, Excited, Relaxed, Romantic (5 moods as per requirement)

---

## 3. Database Models

### 3.1 User Model (Django's built-in or custom)

- Standard Django User fields
- Custom fields (optional): profile_picture, bio

### 3.2 Mood Model

```python
- id (PrimaryKey)
- name (CharField) - e.g., "Happy", "Sad", "Excited"
- description (TextField, optional)
- emoji (CharField, optional) - for UI representation
- is_active (BooleanField)
- created_at (DateTimeField)
```

### 3.3 Movie Model

```python
- id (PrimaryKey)
- title (CharField)
- overview (TextField)
- release_date (DateField)
- poster_url (URLField)
- backdrop_url (URLField, optional)
- tmdb_id (IntegerField, unique) # or similar external API ID
- rating (FloatField, optional)
- genre_ids (JSONField, optional) # Array of genre IDs
- external_api_data (JSONField) # Store full API response for future use
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### 3.4 Recommendation Model (User-Movie-Mood Relationship)

```python
- id (PrimaryKey)
- user (ForeignKey to User)
- movie (ForeignKey to Movie)
- mood (ForeignKey to Mood)
- recommended_at (DateTimeField, auto_now_add)
- viewed (BooleanField, default=False)
- user_rating (IntegerField, null=True) # Optional: let users rate recommendations
```

---

## 4. API Endpoints (REST API)

### 4.1 Authentication Endpoints (`/api/auth/`)

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns JWT token)
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/` - Update user profile

### 4.2 Mood Endpoints (`/api/moods/`)

- `GET /api/moods/` - List all active moods
- `GET /api/moods/{id}/` - Get mood details
- `POST /api/moods/` - Create mood (Admin only)
- `PUT /api/moods/{id}/` - Update mood (Admin only)
- `DELETE /api/moods/{id}/` - Delete mood (Admin only)

### 4.3 Movie Endpoints (`/api/movies/`)

- `GET /api/movies/` - List movies (with pagination)
- `GET /api/movies/{id}/` - Get movie details
- `POST /api/movies/recommend/` - **Get movie recommendations based on mood**
  - Request: `{ "mood_id": 1 }`
  - Response: **2 movies** fetched from external API and saved to DB
  - **Note**: Only 2 movies per request to minimize external API load
  - **Note**: Only 2 movies per request to minimize external API load
- `GET /api/movies/search/?q={query}` - Search movies (optional)

### 4.4 Recommendation History Endpoints (`/api/recommendations/`)

- `GET /api/recommendations/` - Get user's recommendation history (paginated)
- `GET /api/recommendations/{id}/` - Get specific recommendation details
- `POST /api/recommendations/{id}/view/` - Mark recommendation as viewed
- `POST /api/recommendations/{id}/rate/` - Rate a recommendation (optional)
- `GET /api/recommendations/by-mood/{mood_id}/` - Get recommendations filtered by mood
- `DELETE /api/recommendations/{id}/` - Delete a recommendation from history

---

## 5. External API Integration

### Recommended APIs:

1. **The Movie Database (TMDB)** - Most popular, free tier

   - API Key required
   - Endpoint: `https://api.themoviedb.org/3/`
   - Documentation: https://www.themoviedb.org/documentation/api

2. **OMDB API** - Alternative option
   - API Key required
   - Endpoint: `http://www.omdbapi.com/`

### Integration Strategy:

- Create a service class in `movies/services.py`
- Map moods to movie genres/keywords for API queries
- **Fetch only 2 movies per request** to minimize API load
- Handle API rate limiting and error responses
- Cache API responses to avoid duplicate API calls for the same movies

### Mood-to-Genre Mapping Example:

- **Happy**: Comedy, Animation
- **Sad**: Drama, Romance
- **Excited**: Action, Adventure, Thriller
- **Relaxed**: Drama, Documentary, Family
- **Romantic**: Romance, Drama

---

## 6. Technology Stack

### Backend:

- Django 4.2+ / Django 5.0
- Django REST Framework (DRF)
- djangorestframework-simplejwt (JWT authentication)
- python-decouple (environment variables)
- requests (HTTP client for external API)

### Database:

- SQLite (development) or PostgreSQL (production)

### Additional Packages:

- python-decouple (environment variables)
- requests (HTTP client for external API)

**Note**: Since frontend uses Django templates (not separate frontend), CORS headers are not needed. Frontend will be simple HTML with Django template tags and basic CSS.

---

## 7. Authentication Strategy

**Dual Authentication Approach** (API-focused with simple template frontend):

### For API Endpoints (REST API):

- **JWT (JSON Web Tokens)** - For API access
  - Access token (short-lived, 15-60 minutes)
  - Refresh token (longer-lived, 7 days)
  - Implemented via `djangorestframework-simplejwt`

### For Django Template Views (Simple Frontend):

- **Session-based Authentication** - Django's built-in auth
  - User logs in via template form
  - Django session manages authentication
  - Simple and secure for template-based views

**Implementation Note**:

- Template views use Django's `@login_required` decorator
- API endpoints use JWT authentication
- Both can coexist in the same project

---

## 8. Implementation Steps

### Phase 1: Project Setup

1. Create Django project and virtual environment
2. Install dependencies (requirements.txt)
3. Configure settings.py (database, installed apps, CORS, JWT)
4. Create apps: accounts, movies, moods
5. Set up environment variables (.env file)

### Phase 2: Database Models

1. Create Mood model
2. Create Movie model
3. Create Recommendation model
4. Run migrations
5. Create superuser for admin panel

### Phase 3: Authentication API

1. Set up JWT authentication
2. Create User registration endpoint
3. Create User login endpoint
4. Create User profile endpoints
5. Test authentication flow

### Phase 4: Moods API

1. Create Mood serializers
2. Create Mood viewsets/views
3. Create Mood URLs
4. Seed initial moods (Happy, Sad, Excited, Relaxed, Romantic)
5. Test mood endpoints

### Phase 5: External API Integration

1. Set up TMDB API service
2. Create mood-to-genre mapping logic
3. Implement movie fetching function (**Fetch only 2 movies per request to minimize API load**)
4. Handle API errors and rate limiting
5. Test external API integration

### Phase 6: Movie Recommendations API

1. Create Movie serializers
2. Create Movie viewsets
3. Implement recommendation endpoint (fetch + save)
4. Create Recommendation model endpoints
5. Test recommendation flow

### Phase 7: Recommendation History API

1. Create Recommendation serializers
2. Create Recommendation viewsets
3. Implement history filtering (by mood, date, etc.)
4. Add pagination
5. Test history endpoints

### Phase 8: Template Views (Simple Frontend)

1. Create base template with navigation
2. Create login/register template views
3. Create mood selection template view
4. Create movie list template view
5. Create recommendation history template view
6. Add simple CSS (flexbox/grid) for layouts
7. Link all templates together with navigation

### Phase 9: Testing & Documentation

1. Write API tests (optional but recommended)
2. Document API endpoints (use DRF's browsable API or Swagger)
3. Test complete user flow (both API and template views)
4. Handle edge cases and errors

---

## 9. Frontend Considerations (For Your Reference)

While the focus is on Django API, your frontend will need:

1. **Landing Page**:

   - Login/Register forms
   - Redirect authenticated users to mood selection

2. **Mood Selection Page**:

   - Display 3-5 mood buttons
   - Each button triggers API call to `/api/movies/recommend/`

3. **Movie List Page**:

   - Display fetched movies
   - Show movie details (poster, title, overview)
   - Optional: Add to favorites/watchlist

4. **History Page**:
   - Display past recommendations
   - Filter by mood
   - Show recommendation dates

---

## 10. Environment Variables (.env)

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# External API
TMDB_API_KEY=your-tmdb-api-key

# JWT Settings (optional, can use defaults)
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # minutes (7 days)
```

---

## 11. API Response Examples

### Registration Response:

```json
POST /api/auth/register/
{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}

Response: 201 Created
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com"
  }
}
```

### Login Response:

```json
POST /api/auth/login/
{
  "username": "user123",
  "password": "securepass123"
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com"
  }
}
```

### Get Recommendations:

```json
POST /api/movies/recommend/
Headers: Authorization: Bearer <access_token>
Body: {
  "mood_id": 1
}

Response: 200 OK
{
  "mood": {
    "id": 1,
    "name": "Happy"
  },
  "movies": [
    {
      "id": 1,
      "title": "The Grand Budapest Hotel",
      "overview": "A story about...",
      "poster_url": "https://...",
      "release_date": "2014-03-28",
      "recommendation_id": 5
    },
    {
      "id": 2,
      "title": "Toy Story",
      "overview": "A story about toys...",
      "poster_url": "https://...",
      "release_date": "1995-11-22",
      "recommendation_id": 6
    }
  ],
  "count": 2
}
```

### Get Recommendation History:

```json
GET /api/recommendations/
Headers: Authorization: Bearer <access_token>

Response: 200 OK
{
  "count": 45,
  "next": "http://api/recommendations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 5,
      "movie": {
        "id": 1,
        "title": "The Grand Budapest Hotel",
        "poster_url": "https://..."
      },
      "mood": {
        "id": 1,
        "name": "Happy"
      },
      "recommended_at": "2024-01-15T10:30:00Z",
      "viewed": false
    },
    ...
  ]
}
```

---

## 12. Security Considerations

1. **Password Security**: Use Django's password hashing (default)
2. **API Key Security**: Store in environment variables, never commit to git
3. **CORS**: Configure allowed origins for production
4. **Rate Limiting**: Implement on API endpoints (optional)
5. **Input Validation**: Use DRF serializers for validation
6. **SQL Injection**: Django ORM protects against this
7. **XSS**: Sanitize user inputs

---

## 13. Testing Strategy (Optional but Recommended)

- Unit tests for models
- API endpoint tests (using DRF's APIClient)
- External API mocking (using `responses` library)
- Test user flows (registration → login → recommendation → history)

---

## 14. Deployment Considerations (Future)

- Use PostgreSQL for production
- Set DEBUG=False
- Configure ALLOWED_HOSTS
- Use environment variables for secrets
- Set up static files serving
- Configure CORS for frontend domain
- Consider using Docker for containerization

---

## Next Steps

1. Review this plan
2. Confirm technology choices (TMDB API, JWT auth, etc.)
3. Start with Phase 1 (Project Setup)
4. Iterate through phases incrementally
5. Test each phase before moving to next

---

## Questions to Consider

1. Which movie API will you use? (TMDB recommended)
2. ~~How many movies per recommendation?~~ **Answer: 2 movies per request** (to minimize API load)
3. Do you want user ratings on recommendations? (Optional)
4. Do you want a watchlist/favorites feature? (Optional)
5. Should recommendations be paginated? (Yes, for history view)
6. Do you want to cache external API responses? (Optional, but recommended to avoid duplicate API calls for same movies)

---

**This plan provides a solid foundation for your ALX capstone project focusing on API endpoints. All core functionality is API-based, making it perfect for demonstrating REST API development skills.**
