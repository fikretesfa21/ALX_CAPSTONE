# API Testing Results

## ✅ Successfully Tested Endpoints

### 1. Moods API (No Authentication Required)
- **GET /api/moods/** ✅
  - Returns all 5 moods: Happy, Sad, Excited, Relaxed, Romantic
  - Status: Working perfectly

### 2. Authentication API
- **POST /api/auth/register/** ✅
  - Successfully creates new users
  - Returns user data with id, username, email
  - Status: Working perfectly

- **POST /api/auth/login/** ✅
  - Successfully authenticates users
  - Creates session cookie
  - Status: Working perfectly

- **GET /api/auth/profile/** ✅
  - Returns authenticated user's profile
  - Requires authentication
  - Status: Working perfectly

## ⚠️ Endpoints Requiring Browser Testing

Due to CSRF protection with session authentication, POST/DELETE endpoints are best tested via the Django REST Framework browsable API in a browser:

### Movie Recommendation API
- **POST /api/movies/recommend/** - Requires browser (CSRF token handled automatically)
- **GET /api/movies/** - Should work with curl (GET request)
- **GET /api/movies/recommendations/** - Should work with curl (GET request)
- **POST /api/movies/recommendations/{id}/view/** - Requires browser
- **DELETE /api/movies/recommendations/{id}/delete/** - Requires browser

## How to Test in Browser

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Navigate to API endpoints in your browser:**
   - List moods: http://127.0.0.1:8000/api/moods/
   - Register: http://127.0.0.1:8000/api/auth/register/
   - Login: http://127.0.0.1:8000/api/auth/login/
   - Get recommendations: http://127.0.0.1:8000/api/movies/recommend/
   - View history: http://127.0.0.1:8000/api/movies/recommendations/

3. **The DRF browsable API will:**
   - Show a form for POST requests
   - Handle CSRF tokens automatically
   - Allow you to submit requests directly from the browser

## Test the Movie Recommendation Endpoint

1. Make sure your `.env` file has your TMDB_API_KEY
2. Login first: http://127.0.0.1:8000/api/auth/login/
3. Then go to: http://127.0.0.1:8000/api/movies/recommend/
4. Fill in the form with:
   ```json
   {
     "mood_id": 1
   }
   ```
5. Click POST button
6. You should see 2 movies fetched from TMDB!

## Mood IDs Reference
- 1 = Happy
- 2 = Sad
- 3 = Excited
- 4 = Relaxed
- 5 = Romantic

