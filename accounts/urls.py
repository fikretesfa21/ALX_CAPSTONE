from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Template views (HTML frontend)
    path('register/', views.register_template_view, name='register'),
    path('login/', views.login_template_view, name='login'),
    path('logout/', views.logout_template_view, name='logout'),
]

