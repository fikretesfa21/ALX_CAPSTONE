from django.urls import path
from . import views

app_name = 'moods'

urlpatterns = [
    path('', views.mood_list_view, name='mood-list'),
    path('<int:pk>/', views.mood_detail_view, name='mood-detail'),
]

