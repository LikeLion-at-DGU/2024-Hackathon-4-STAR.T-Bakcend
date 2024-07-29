from rest_framework import serializers
from .models import Theme
from celeb.models import Celeb
from routine.models import Routine

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'title', 'content', 'image']

class CelebritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Celeb
        fields = ['id', 'name', 'profession']

class RoutineSerializer(serializers.ModelSerializer):
    celeb = serializers.CharField(source='celeb.name')
    
    category = serializers.SlugRelatedField(
    many=True,
    read_only=True,
    slug_field='name'
    )
    
    theme = serializers.SlugRelatedField(
    many=True,
    read_only=True,
    slug_field='title'
    )
    class Meta:
        model = Routine
        fields = ['id', 'title', 'sub_title', 'content', 'category', 'celeb', 'image', 'video_url','theme']
