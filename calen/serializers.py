from rest_framework import serializers
from .models import Calendar, CalendarRoutine

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = [
            'id',
            'user',
            'date',
            'title'
        ]

class CalendarRoutineSerializer(serializers.ModelSerializer):
    calendar = CalendarSerializer()

    class Meta:
        model = CalendarRoutine
        fields = [
            'id',
            'calendar',
            'routine',
            'status',
        ]

    # def create(self, validated_data):
    #     calendar_data = validated_data.pop('calendar')
    #     calendar = Calendar.objects.create(**calendar_data)
    #     calendar_routine = CalendarRoutine.objects.create(calendar=calendar, **validated_data)
    #     return calendar_routine
