from rest_framework import serializers
from .models import Celeb
from rank.models import CelebScore
from routine.serializers import RoutineSerializer
from routine.models import Routine
from calen.models import UserRoutine, UserRoutineCompletion

class CelebScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CelebScore
        fields = ['celeb', 'score', 'completed']

class CelebSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField()
    routines = serializers.SerializerMethodField()
    routines_count = serializers.SerializerMethodField()
    routines_added_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Celeb
        fields = '__all__'

    def get_routines_count(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return {'user_count': 0, 'total_count': 0}
        
        user = request.user
        # 사용자가 수행한 루틴 수
        user_routines_count = UserRoutine.objects.filter(routine__celeb=obj, user=user).count()
        # 총 루틴 수
        total_routines_count = Routine.objects.filter(celebrity=obj).count()
        
        return {
            'user_count': user_routines_count,
            'total_count': total_routines_count
        }

    def get_routines_added_count(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return 0
        
        user = request.user

        # 사용자가 추가한 후 완료된 루틴 횟수
        routines_added_count = UserRoutine.objects.filter(
            routine__celeb=obj,
            user=user,
            userroutinecompletion__completed=True,
        ).distinct().count()
        
        return routines_added_count

    def get_scores(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return []
        
        user = request.user
        scores = CelebScore.objects.filter(celeb=obj, user=user)
        return CelebScoreSerializer(scores, many=True).data

    def get_routines(self, obj):
        routines = Routine.objects.filter(celebrity=obj)
        return RoutineSerializer(routines, many=True).data