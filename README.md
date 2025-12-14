# 🎬 MoodFlicks

**"I’m feeling nostalgic → here are 3 iconic 90s comedies you can stream right now."**

MoodFlicks is a movie recommendation platform that cuts through decision paralysis by asking the only question that matters: *"How are you feeling?"*

## 🚀 The Problem
*   **Decision Paralysis**: Streaming services offer thousands of titles, leading to "doom-scrolling" instead of watching.
*   **Context Disconnect**: Algorithms suggest what you *might* like based on history, not what you *need* right now (e.g., cheering up after a bad day).
*   **Weather ≠ Mood**: While some apps use weather, mood is specific, personal, and actionable.

## 💡 The Solution
A streamlined interface that maps human emotions directly to cinema genres.
1.  **Input**: Users select a mood (e.g., Happy, Sad, Chill).
2.  **Process**: The backend translates this into complex TMDb queries (Genres + Decades + Keywords).
3.  **Output**: Users get **3 hand-picked recommendations** available to stream, instantly.

## ✨ Key Features

### 🎭 Mood-Based Filtering
Six distinct moods mapped to specific cinematic recipes:
*   **Happy**: High-rated Comedies to lift spirits.
*   **Sad**: Dramas and Romances for a good cry (Keyword: "bittersweet").
*   **Nostalgic**: 90s/00s classics that feel like home.
*   **Pumped**: Action & Adventure for high energy.
*   **Chill**: Slow-burn Mysteries and Crime thrillers.
*   **Curious**: Top-rated Documentaries.

### ⚡ Instant Gratification
*   **No Scrolling**: We show only 3 top recommendations.
*   **Smart Caching**: Results are cached for 1 hour to ensure speed while keeping content fresh.

### 📺 Streaming Availability
*   **Where to Watch**: Instantly see which streaming service (Netflix, Amazon, etc.) has the movie in your region (via TMDb).

### 📝 Watchlist Management
*   **Save for Later**: Authenticated users can add movies to their personal watchlist.
*   **Contextual Saving**: Remembers the mood you were in when you added it.
*   **Export Data**: Download your entire watchlist as a CSV file to share or keep.

## 🛠️ Technology Stack
*   **Backend**: Django + Django REST Framework (DRF)
*   **Database**: PostgreSQL / SQLite (Dev)
*   **Frontend**: HTML Templates + **Tailwind CSS** (Styling) + **HTMX** (Dynamic interactions)
*   **APIs**: TMDb (Discovery/Providers) + OMDb (Ratings/Posters)
*   **Infrastructure**: Docker + Redis (Caching)
