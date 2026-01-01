# Movieflick - Movie Recommendation Platform

A Django-based movie recommendation platform that suggests movies based on user moods.

## Features

- User authentication (registration/login)
- Mood-based movie recommendations (5 moods: Happy, Sad, Excited, Relaxed, Romantic)
- Integration with TMDB API for movie data
- Recommendation history tracking
- RESTful API endpoints

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

Get your TMDB API key from: https://www.themoviedb.org/settings/api

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
movieflick/
├── accounts/          # User authentication app
├── movies/            # Movie recommendations app
├── moods/             # Mood management app
├── movieflick/        # Main project settings
├── templates/         # HTML templates
├── static/            # Static files (CSS, etc.)
└── manage.py
```

## API Endpoints

(API endpoints will be documented here as they are implemented)

## Technology Stack

- Django 5.0
- Django REST Framework
- SQLite (development database)
- TMDB API
