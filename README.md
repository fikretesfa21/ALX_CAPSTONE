# Movieflick - Movie Recommendation Platform 🎬

A Django-based movie recommendation platform that suggests movies based on user moods. This project demonstrates backend proficiency with REST API endpoints and includes a simple HTML frontend interface.

## Features

- ✅ User authentication (registration/login/logout)
- ✅ 5 mood-based movie recommendations (Happy, Sad, Excited, Relaxed, Romantic)
- ✅ TMDB API integration (fetches 2 movies per mood)
- ✅ Movie data stored in database
- ✅ Recommendation history tracking
- ✅ RESTful API endpoints (JSON)
- ✅ Simple HTML frontend with Django templates
- ✅ Responsive CSS styling (Flexbox/Grid)

## Technology Stack

- **Backend:** Django 5.0
- **API Framework:** Django REST Framework
- **Database:** SQLite (development)
- **External API:** TMDB (The Movie Database)
- **Frontend:** HTML, Django Templates, CSS (Flexbox/Grid)
- **Authentication:** Django session authentication

## Project Structure

```
movieflick/
├── accounts/              # User authentication app
│   ├── views.py          # API + template views
│   ├── urls.py           # Template URLs
│   └── urls_api.py       # API URLs
├── movies/               # Movie recommendations app (main app)
│   ├── views.py          # API + template views
│   ├── services.py       # TMDB API integration
│   ├── models.py         # Movie, Recommendation models
│   ├── urls.py           # Template URLs
│   └── urls_api.py       # API URLs
├── moods/                # Mood management app
│   ├── models.py         # Mood model
│   └── urls.py           # Mood API URLs
├── templates/            # HTML templates
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── movies/
│       ├── mood_selection.html
│       ├── movie_list.html
│       └── recommendation_history.html
├── static/               # Static files
│   └── css/
│       └── style.css
├── movieflick/           # Main project settings
└── manage.py
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd movieflick
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
TMDB_API_KEY=your-tmdb-api-key-here
```

**Get your TMDB API key:** https://www.themoviedb.org/settings/api

### 5. Run migrations

```bash
python manage.py migrate
```

This will create the database and seed the 5 moods (Happy, Sad, Excited, Relaxed, Romantic).

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Frontend (HTML Interface)

1. **Access the application:** http://127.0.0.1:8000/
2. **Register/Login:** Create an account or login
3. **Select a mood:** Choose from 5 available moods
4. **View recommendations:** See 2 movies recommended based on your mood
5. **View history:** Check your past recommendations

### API Endpoints (JSON)

#### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

#### Moods

- `GET /api/moods/` - List all active moods
- `GET /api/moods/<id>/` - Get mood details

#### Movies

- `GET /api/movies/` - List all movies
- `GET /api/movies/<id>/` - Get movie details
- `POST /api/movies/recommend/` - Get movie recommendations by mood
  ```json
  {
    "mood_id": 1
  }
  ```

#### Recommendations

- `GET /api/movies/recommendations/` - Get user's recommendation history
- `GET /api/movies/recommendations/<id>/` - Get recommendation details
- `POST /api/movies/recommendations/<id>/view/` - Mark recommendation as viewed
- `DELETE /api/movies/recommendations/<id>/delete/` - Delete recommendation

### Mood IDs

- 1 = Happy (Comedy, Animation)
- 2 = Sad (Drama, Romance)
- 3 = Excited (Action, Adventure, Thriller)
- 4 = Relaxed (Drama, Documentary, Family)
- 5 = Romantic (Romance, Drama)

## API Testing

### Using curl

**Register:**

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123", "password2": "testpass123"}'
```

**Login:**

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Get Recommendations:**

```bash
curl -X POST http://127.0.0.1:8000/api/movies/recommend/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"mood_id": 1}'
```

### Using Django REST Framework Browsable API

Navigate to any API endpoint in your browser (e.g., `http://127.0.0.1:8000/api/moods/`) to use the interactive API interface.

## Key Implementation Details

- **Movie Fetching:** Only 2 movies per request to minimize TMDB API load
- **Mood-to-Genre Mapping:** Each mood maps to specific TMDB genre IDs
- **Dual Views:** Both API (JSON) and template (HTML) views coexist
- **Simple Frontend:** Clean HTML with Django template tags, basic CSS (no JavaScript frameworks)
- **Session Authentication:** Django's built-in session authentication for both API and templates

## Author

Movieflick - Movie Recommendation Platform
