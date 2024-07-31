from rest_framework import serializers
from .models import Routine, RoutineCategory


class RoutineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineCategory
        fields = '__all__'


class RoutineSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    celebrity = serializers.SlugRelatedField(
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
        fields = ['id', 'title', 'sub_title', 'content', 'image', 'video_url', 'category', 'celebrity', 'theme']