# accounts/serializers.py
from rest_framework import serializers
from .models import User
from routine.models import RoutineCategory
from rank.models import CelebScore
from rank.serializers import MypageCelebSerializer
from calen.models import UserRoutine
from celeb.models import Celeb

class UserSerializer(serializers.ModelSerializer):
    is_new_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'is_new_user', 'nickname']

    def get_is_new_user(self, obj):
        return obj.is_new_user()
    

class CustomRoutineSerializer(serializers.Serializer):
    preferred_routine_categories = serializers.PrimaryKeyRelatedField(queryset=RoutineCategory.objects.all(), many=True)

    def validate_preferred_routine_categories(self, value):
        if not value:
            raise serializers.ValidationError("Preferred routine categories are required.")
        return value
    

class UserProfileSerializer(serializers.ModelSerializer):
    celebs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['nickname', 'celebs']

    def get_celebs(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return []

        user = request.user

        celebs = Celeb.objects.all()
        sorted_celebs = sorted(celebs, key=lambda celeb: MypageCelebSerializer(context={'request': request}).get_routines_added_count(celeb), reverse=True)
        top_celebs = sorted_celebs[:3]

        return MypageCelebSerializer(top_celebs, many=True, context={'request': request}).data
    

class NicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['nickname']