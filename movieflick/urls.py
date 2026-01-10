
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    # API endpoints
    path('api/auth/', include('accounts.urls_api')),
    path('api/moods/', include('moods.urls')),
    path('api/movies/', include('movies.urls_api')),
    # Template views (HTML frontend)
    path('auth/', include('accounts.urls')),
    path('movies/', include('movies.urls')),
]
