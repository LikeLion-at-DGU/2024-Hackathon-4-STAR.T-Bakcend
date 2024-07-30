from rest_framework import serializers
from .models import CelebScore

from rest_framework import serializers
from .models import CelebScore

class CelebScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CelebScore
        fields = '__all__'
