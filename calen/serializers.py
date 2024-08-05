from rest_framework import serializers
from .models import UserRoutine, PersonalSchedule, MonthlyTitle, UserRoutineCompletion

from routine.serializers import RoutineSerializer
from datetime import date


class UserRoutineSerializer(serializers.ModelSerializer):
    routine_title = serializers.CharField(source='routine.title')
    routine_content = serializers.CharField(source='routine.content')
    completed = serializers.SerializerMethodField()
    popular = serializers.IntegerField(source='routine.popular', read_only=True) 
    celebrity_id = serializers.IntegerField(source='routine.celebrity.id', read_only=True)  # 셀럽 ID 필드 추가

    class Meta:
        model = UserRoutine
        fields = '__all__' 

    def get_completed(self, obj):
        # context에서 request를 가져옵니다
        request = self.context.get('request')
        if request is None:
            return False

        user = request.user
        selected_date = self.context.get('selected_date')

        completions = UserRoutineCompletion.objects.filter(
            user=user,
            routine=obj,
            completed=True
        )

        for completion in completions:
            if completion.date == selected_date:
                return True

        return False

class PersonalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = '__all__'

        extra_kwargs = {
                'title': {'required': False},   # 선택적 필드
                'description': {'required': False},  # 선택적 필드
            }

class MonthlyTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyTitle
        fields = '__all__'

class UserRoutineCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoutineCompletion
        fields = '__all__'