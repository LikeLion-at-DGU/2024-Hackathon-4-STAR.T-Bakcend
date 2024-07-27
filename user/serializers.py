from rest_framework import serializers
from .models import User
from routine.models import RoutineCategory

class UserSerializer(serializers.ModelSerializer):
    preferred_routine_categories = serializers.SlugRelatedField(
        many=True,
        queryset=RoutineCategory.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'social_login_type', 'subscription_status', 'subscription_expiry_date', 'preferred_routine_categories', 'code']
