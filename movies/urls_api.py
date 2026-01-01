from django.urls import path
from . import views

# API URLs - no app_name needed as it's only included once
urlpatterns = [
    # Movie endpoints
    path('', views.movie_list_view, name='movie-list'),
    path('<int:pk>/', views.movie_detail_view, name='movie-detail'),
    
    # Recommendation endpoints
    path('recommend/', views.recommend_movies_view, name='movie-recommend'),
    path('recommendations/', views.recommendation_history_view, name='recommendation-history'),
    path('recommendations/<int:pk>/', views.recommendation_detail_view, name='recommendation-detail'),
    path('recommendations/<int:pk>/view/', views.mark_recommendation_viewed_view, name='mark-recommendation-viewed'),
    path('recommendations/<int:pk>/delete/', views.delete_recommendation_view, name='delete-recommendation'),
]

