# API Testing Guide

This guide helps you test all the API endpoints for Movieflick.

## Prerequisites

1. Make sure you have a `.env` file in the project root with:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   TMDB_API_KEY=your-tmdb-api-key-here
   ```

2. Start the development server:
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

3. The API will be available at: `http://127.0.0.1:8000/api/`

## Testing Endpoints

### 1. Test Moods API (No Authentication Required)

**List all moods:**
```bash
curl http://127.0.0.1:8000/api/moods/
```

**Get mood details:**
```bash
curl http://127.0.0.1:8000/api/moods/1/
```

### 2. Test Authentication API

**Register a new user:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Get profile (after login):**
```bash
curl http://127.0.0.1:8000/api/auth/profile/ \
  -b cookies.txt
```

**Logout:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -b cookies.txt
```

### 3. Test Movies API (Authentication Required)

**Get movie recommendations (mood_id 1 = Happy):**
```bash
curl -X POST http://127.0.0.1:8000/api/movies/recommend/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "mood_id": 1
  }'
```

**List all movies:**
```bash
curl http://127.0.0.1:8000/api/movies/ \
  -b cookies.txt
```

**Get recommendation history:**
```bash
curl http://127.0.0.1:8000/api/movies/recommendations/ \
  -b cookies.txt
```

**Get recommendation details:**
```bash
curl http://127.0.0.1:8000/api/movies/recommendations/1/ \
  -b cookies.txt
```

**Mark recommendation as viewed:**
```bash
curl -X POST http://127.0.0.1:8000/api/movies/recommendations/1/view/ \
  -b cookies.txt
```

**Delete a recommendation:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/movies/recommendations/1/delete/ \
  -b cookies.txt
```

## Testing with Django REST Framework Browsable API

Django REST Framework provides a browsable API interface. You can:

1. Navigate to any endpoint in your browser (e.g., `http://127.0.0.1:8000/api/moods/`)
2. Use the interface to make GET requests directly
3. For POST requests, you'll need to login first via the login endpoint

## Testing Flow Example

1. **Register a user:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "demo", "email": "demo@test.com", "password": "demo123", "password2": "demo123"}'
   ```

2. **Login:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -c cookies.txt \
     -d '{"username": "demo", "password": "demo123"}'
   ```

3. **Get moods list:**
   ```bash
   curl http://127.0.0.1:8000/api/moods/
   ```

4. **Get movie recommendations for mood 1 (Happy):**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/movies/recommend/ \
     -H "Content-Type: application/json" \
     -b cookies.txt \
     -d '{"mood_id": 1}'
   ```

5. **View recommendation history:**
   ```bash
   curl http://127.0.0.1:8000/api/movies/recommendations/ \
     -b cookies.txt
   ```

## Mood IDs Reference

1. Happy (Comedy, Animation)
2. Sad (Drama, Romance)
3. Excited (Action, Adventure, Thriller)
4. Relaxed (Drama, Documentary, Family)
5. Romantic (Romance, Drama)

## Notes

- Session-based authentication uses cookies, so make sure to use `-c cookies.txt` (save) and `-b cookies.txt` (use) with curl
- All movie endpoints require authentication except for moods endpoints
- The recommendation endpoint fetches 2 movies from TMDB API each time it's called
- Make sure your TMDB_API_KEY is set in the .env file

