# Generated migration - Seed initial moods

from django.db import migrations


def create_initial_moods(apps, schema_editor):
    """Create the 5 fixed moods"""
    Mood = apps.get_model('moods', 'Mood')
    
    moods_data = [
        {
            'name': 'Happy',
            'description': 'Feel-good movies that will brighten your day',
            'emoji': '😊',
            'is_active': True,
        },
        {
            'name': 'Sad',
            'description': 'Emotional and dramatic films',
            'emoji': '😢',
            'is_active': True,
        },
        {
            'name': 'Excited',
            'description': 'Action-packed and thrilling movies',
            'emoji': '🎬',
            'is_active': True,
        },
        {
            'name': 'Relaxed',
            'description': 'Calm and peaceful films to unwind with',
            'emoji': '😌',
            'is_active': True,
        },
        {
            'name': 'Romantic',
            'description': 'Love stories and romantic films',
            'emoji': '❤️',
            'is_active': True,
        },
    ]
    
    for mood_data in moods_data:
        Mood.objects.get_or_create(
            name=mood_data['name'],
            defaults=mood_data
        )


def reverse_moods(apps, schema_editor):
    """Remove the seeded moods"""
    Mood = apps.get_model('moods', 'Mood')
    Mood.objects.filter(
        name__in=['Happy', 'Sad', 'Excited', 'Relaxed', 'Romantic']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('moods', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_moods, reverse_moods),
    ]
