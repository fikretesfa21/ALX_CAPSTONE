from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Mood

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['name', 'slug', 'icon']

class MoodListView(ListAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = [AllowAny]
