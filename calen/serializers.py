from rest_framework import serializers
from .models import UserRoutine, PersonalSchedule, MonthlyTitle

class UserRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoutine
        fields = '__all__'

class PersonalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalSchedule
        fields = '__all__'

class MonthlyTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyTitle
        fields = '__all__'