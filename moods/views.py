from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Mood
from .serializers import MoodSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def mood_list_view(request):
    """List all active moods"""
    moods = Mood.objects.filter(is_active=True)
    serializer = MoodSerializer(moods, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def mood_detail_view(request, pk):
    """Get mood details by ID"""
    try:
        mood = Mood.objects.get(pk=pk, is_active=True)
    except Mood.DoesNotExist:
        return Response(
            {'error': 'Mood not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = MoodSerializer(mood)
    return Response(serializer.data, status=status.HTTP_200_OK)
