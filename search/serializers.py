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
        fields = ['id', 'name', 'category', 'profession']

class RoutineSerializer(serializers.ModelSerializer):
    celebrity = serializers.CharField(source='celebrity.name')

    class Meta:
        model = Routine
        fields = ['id', 'title', 'sub_title', 'content', 'category', 'celebrity', 'image', 'video_url']
