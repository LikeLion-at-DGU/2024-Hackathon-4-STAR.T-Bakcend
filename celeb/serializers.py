from rest_framework import serializers
from .models import Celeb
from rank.models import CelebScore
from routine.serializers import RoutineSerializer
from routine.models import Routine

class CelebScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CelebScore
        fields = '__all__'

class CelebSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField()
    routines = serializers.SerializerMethodField()
    
    class Meta:
        model = Celeb
        fields = '__all__'

    def get_routines(self, obj):
        # routines = obj.routines.all()
        routines = Routine.objects.filter(celebrity=obj)
        return RoutineSerializer(routines, many=True).data

    def get_scores(self, obj):
        user = self.context['request'].user
        scores = CelebScore.objects.filter(celeb=obj, user=user)
        return CelebScoreSerializer(scores, many=True).data