from rest_framework import serializers
from .models import CelebScore
from celeb.serializers import CelebSerializer


class CelebScoreSerializer(serializers.ModelSerializer):
    celeb = CelebSerializer()
    class Meta:
        model = CelebScore
        fields = ['id','score','celeb']