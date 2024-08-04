from rest_framework import serializers
from .models import UserRoutine, PersonalSchedule, MonthlyTitle, UserRoutineCompletion

from routine.serializers import RoutineSerializer
from datetime import date


class UserRoutineSerializer(serializers.ModelSerializer):
    routine_title = serializers.CharField(source='routine.title')
    routine_content = serializers.CharField(source='routine.content')
    completed = serializers.SerializerMethodField()
    popular = serializers.IntegerField(source='routine.popular', read_only=True) 

    class Meta:
        model = UserRoutine
        fields = '__all__' 

    def get_completed(self, obj):
        user = self.context['request'].user
        
        completions = UserRoutineCompletion.objects.filter(
            user=user,
            routine=obj,
            completed=True
        )
        
        for completion in completions:
            if completion.date == self.context.get('selected_date'):
                return True
        
        return False

class PersonalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class MonthlyTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyTitle
        fields = '__all__'

class UserRoutineCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoutineCompletion
        fields = '__all__'