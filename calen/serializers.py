from rest_framework import serializers
from .models import UserRoutine, PersonalSchedule, MonthlyTitle, UserRoutineCompletion

from routine.serializers import RoutineSerializer
from datetime import date


class UserRoutineSerializer(serializers.ModelSerializer):
    routine_title = serializers.CharField(source='routine.title')
    routine_content = serializers.CharField(source='routine.content')
    completed = serializers.SerializerMethodField()  # 완료 여부를 추가하는 필드

    class Meta:
        model = UserRoutine
        fields = '__all__'  # 모든 필드를 포함하지만, completed는 get_completed 메서드로 설정

    def get_completed(self, obj):
        user = self.context['request'].user
        
        # 루틴의 완료 여부를 확인
        completions = UserRoutineCompletion.objects.filter(
            user=user,
            routine=obj,
            completed=True
        )
        
        # 루틴의 기간에 대한 완료 여부 확인
        for completion in completions:
            if completion.date == self.context.get('selected_date'):
                return True
        
        return False

class PersonalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = '__all__'

class MonthlyTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyTitle
        fields = '__all__'

class UserRoutineCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoutineCompletion
        fields = '__all__'