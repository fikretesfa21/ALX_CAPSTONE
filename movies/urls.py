from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # Template views (HTML frontend)
    path('moods/', views.mood_selection_template_view, name='mood-selection'),
    path('recommend/<int:mood_id>/', views.get_recommendations_template_view, name='get-recommendations'),
    path('history/', views.recommendation_history_template_view, name='recommendation-history'),
]

