# API Testing Instructions

## Testing the Movie Recommendation Endpoint

When testing the `/api/movies/recommend/` endpoint in the DRF browsable API, you have two options:

### Option 1: Use the HTML Form (Easiest)

1. Navigate to: http://127.0.0.1:8000/api/movies/recommend/
2. Make sure you're logged in first (see login instructions below)
3. In the HTML form, enter:
   - **mood_id**: `1` (just the number, no quotes, no JSON)
4. Click the "POST" button

### Option 2: Use Raw Data (JSON)

1. Navigate to: http://127.0.0.1:8000/api/movies/recommend/
2. Make sure you're logged in first
3. Click on the "Raw data" tab
4. Select "application/json" from the content type dropdown
5. Enter JSON:
   ```json
   {
     "mood_id": 1
   }
   ```
6. Click "POST"

## How to Login First

1. Go to: http://127.0.0.1:8000/api/auth/login/
2. Use the HTML form:
   - **username**: `testuser`
   - **password**: `testpass123`
   - Click "POST"
3. After successful login, you'll be authenticated for other endpoints

Or use Raw data (JSON):
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

## Mood IDs
- 1 = Happy
- 2 = Sad  
- 3 = Excited
- 4 = Relaxed
- 5 = Romantic

## Quick Test Flow

1. **Login**: http://127.0.0.1:8000/api/auth/login/
   - username: `testuser`, password: `testpass123`

2. **Get Recommendations**: http://127.0.0.1:8000/api/movies/recommend/
   - mood_id: `1` (in the form field, not JSON)
   - Click POST

3. **View History**: http://127.0.0.1:8000/api/movies/recommendations/

4. **List All Movies**: http://127.0.0.1:8000/api/movies/

