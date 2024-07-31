# accounts/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    is_new_user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'is_new_user']

    def get_is_new_user(self, obj):
        return obj.is_new_user()
