from django.contrib import admin
from .models import Mood


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'emoji', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
