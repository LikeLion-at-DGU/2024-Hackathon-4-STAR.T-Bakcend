from rest_framework import serializers
from .models import CelebScore
from celeb.serializers import CelebSerializer,MypageCelebSerializer


class CelebScoreSerializer(serializers.ModelSerializer):
    celeb = CelebSerializer()
    class Meta:
        model = CelebScore
        fields = ['id','score','celeb']

# class MypageSocreSerizalizer(serializers.ModelSerializer):
#     celeb = MypageCelebSerializer()
#     class Meta:
#         model = CelebScore
#         fields = ['score','celeb']