from django.db import models

class Mood(models.Model):
    name = models.CharField(max_length=50) 
    slug = models.SlugField(unique=True) 
    icon = models.CharField(max_length=50, blank=True) 
    

    genre_ids = models.JSONField(default=list, help_text="List of TMDb genre IDs (OR logic)")
    

    keywords = models.JSONField(default=list, blank=True, help_text="List of keyword strings or IDs")
    
    min_rating = models.FloatField(default=0.0, help_text="Minimum vote_average")
    year_start = models.IntegerField(null=True, blank=True)
    year_end = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
