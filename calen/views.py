from datetime import date, timedelta
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils.dateparse import parse_date

from .models import UserRoutine, PersonalSchedule, MonthlyTitle
from .serializers import UserRoutineSerializer, PersonalScheduleSerializer, MonthlyTitleSerializer

class CalendarViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def monthly(self, request):
        user = request.user
        month_str = request.query_params.get('month')
        if month_str:
            month = parse_date(month_str)
        else:
            month = date.today().replace(day=1)

        # 해당 월의 첫날과 마지막 날 계산
        first_day = month
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1))

        # 해당 월의 루틴과 개인 일정을 가져옴
        routines = UserRoutine.objects.filter(
            user=user,
            start_date__lte=last_day,
            end_date__gte=first_day
        )
        schedules = PersonalSchedule.objects.filter(
            user=user,
            date__range=[first_day, last_day]
        )
        title = MonthlyTitle.objects.filter(user=user, month=first_day).first()

        return Response({
            'month': first_day.strftime('%Y-%m'),
            'title': title.title if title else '',
            'routines': UserRoutineSerializer(routines, many=True).data,
            'schedules': PersonalScheduleSerializer(schedules, many=True).data
        })

    @action(detail=False, methods=['get'])
    def weekly(self, request):
        user = request.user
        start_date_str = request.query_params.get('start_date')
        if start_date_str:
            start_date = parse_date(start_date_str)
        else:
            start_date = date.today()

        # 해당 주의 첫날과 마지막 날 계산
        first_day = start_date - timedelta(days=start_date.weekday())
        last_day = first_day + timedelta(days=6)

        # 해당 주의 루틴과 개인 일정을 가져옴
        routines = UserRoutine.objects.filter(
            user=user,
            start_date__lte=last_day,
            end_date__gte=first_day
        )
        schedules = PersonalSchedule.objects.filter(
            user=user,
            date__range=[first_day, last_day]
        )

        return Response({
            'week': first_day.strftime('%Y-%m-%d') + ' to ' + last_day.strftime('%Y-%m-%d'),
            'routines': UserRoutineSerializer(routines, many=True).data,
            'schedules': PersonalScheduleSerializer(schedules, many=True).data
        })
