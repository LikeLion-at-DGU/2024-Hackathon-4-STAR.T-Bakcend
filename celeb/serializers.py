from rest_framework import serializers
from .models import Celeb
from rank.models import CelebScore
from routine.serializers import RoutineSerializer
from routine.models import Routine
from calen.models import UserRoutine, UserRoutineCompletion
from django.db.models import Count, Q
from datetime import timedelta

class CelebScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CelebScore
        fields = ['celeb', 'score']

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
        # 수정된 부분: UserRoutine에서 routine__celebrity를 참조하도록 변경
        user_routines_count = UserRoutine.objects.filter(routine__celebrity=obj, user=user).values_list('routine_id', flat=True).distinct().count()
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

        user_routines = UserRoutine.objects.filter(
            routine__celebrity=obj,
            user=user,
        )

        routines_added_count = 0

        for user_routine in user_routines:
            routine_dates = [user_routine.start_date + timedelta(days=i) for i in range((user_routine.end_date - user_routine.start_date).days + 1)]
            
            completed_dates = UserRoutineCompletion.objects.filter(
                user=user,
                routine=user_routine,
                date__in=routine_dates,
                completed=True
            ).values_list('date', flat=True)
            
            if set(routine_dates) == set(completed_dates):
                routines_added_count += 1
        
        return routines_added_count
        
        # [2번 경우의 수] : 기간 중 체킹한게 존재하기만 하면 횟수 증가
        '''
        routines_added_count = UserRoutine.objects.filter(
            routine__celebrity=obj,
            user=user,
            completions__completed=True,
        ).distinct().count()
        
        return routines_added_count
        '''

    def get_scores(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return []
        
        user = request.user
        scores = CelebScore.objects.filter(celeb=obj, user=user)
        return CelebScoreSerializer(scores, many=True).data

    def get_routines(self, obj):
        # Routine에서 celebrity 필드를 참조하여 필터링
        routines = Routine.objects.filter(celebrity=obj)
        return RoutineSerializer(routines, many=True).data

class MypageCelebSerializer(serializers.ModelSerializer):
    routines_added_count = serializers.SerializerMethodField()

    class Meta:
        model = Celeb
        fields = ['id', 'name', 'profession', 'photo', 'routines_added_count']

    def get_routines_added_count(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return 0

        user = request.user

        # 수정된 부분: UserRoutine에서 routine__celebrity를 참조하도록 변경
        routines_added_count = UserRoutine.objects.filter(
            routine__celebrity=obj,
            user=user,
            completions__completed=True,
        ).distinct().count()

        return routines_added_count