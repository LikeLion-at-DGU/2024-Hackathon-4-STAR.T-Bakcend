# accounts/serializers.py
from rest_framework import serializers
from .models import User
from routine.models import RoutineCategory

class UserSerializer(serializers.ModelSerializer):
    is_new_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'is_new_user']

    def get_is_new_user(self, obj):
        return obj.is_new_user()
    

class CustomRoutineSerializer(serializers.Serializer):
    preferred_routine_categories = serializers.PrimaryKeyRelatedField(queryset=RoutineCategory.objects.all(), many=True)

    def validate_preferred_routine_categories(self, value):
        if not value:
            raise serializers.ValidationError("Preferred routine categories are required.")
        return value