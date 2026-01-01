#!/bin/bash
# Quick test script for API endpoints
# Make sure the server is running: python manage.py runserver

BASE_URL="http://127.0.0.1:8000/api"
COOKIE_FILE="test_cookies.txt"

echo "========================================="
echo "Testing Movieflick API Endpoints"
echo "========================================="
echo ""

# Test 1: List Moods (No auth required)
echo "1. Testing GET /api/moods/ (No auth required)..."
curl -s -X GET "$BASE_URL/moods/" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 2: Register a test user
echo "2. Testing POST /api/auth/register/..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }')
echo "$REGISTER_RESPONSE" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 3: Login
echo "3. Testing POST /api/auth/login/..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -c "$COOKIE_FILE" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }')
echo "$LOGIN_RESPONSE" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 4: Get Profile (requires auth)
echo "4. Testing GET /api/auth/profile/ (requires auth)..."
curl -s -X GET "$BASE_URL/auth/profile/" -b "$COOKIE_FILE" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 5: Get Movie Recommendations (requires auth + TMDB API key)
echo "5. Testing POST /api/movies/recommend/ (requires auth)..."
RECOMMEND_RESPONSE=$(curl -s -X POST "$BASE_URL/movies/recommend/" \
  -H "Content-Type: application/json" \
  -b "$COOKIE_FILE" \
  -d '{
    "mood_id": 1
  }')
echo "$RECOMMEND_RESPONSE" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 6: Get Recommendation History
echo "6. Testing GET /api/movies/recommendations/..."
curl -s -X GET "$BASE_URL/movies/recommendations/" -b "$COOKIE_FILE" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo "========================================="
echo "Testing Complete!"
echo "========================================="
echo ""
echo "Note: Make sure the server is running: python manage.py runserver"
echo "Clean up: rm -f $COOKIE_FILE"

