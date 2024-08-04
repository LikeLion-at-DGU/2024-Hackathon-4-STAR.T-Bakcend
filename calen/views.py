from datetime import date, timedelta
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q

from .models import UserRoutine, PersonalSchedule, MonthlyTitle, UserRoutineCompletion
from .serializers import UserRoutineSerializer, PersonalScheduleSerializer, MonthlyTitleSerializer, UserRoutineCompletionSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from routine.models import Routine
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from datetime import datetime

from collections import defaultdict


class CalendarViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        user = request.user
        if not user.is_authenticated:
            return None
        return user
    
    @action(detail=False, methods=['get'])
    def daily(self, request, date=None):
        date_obj = parse_date(date)
        if not date_obj:
            return Response({"detail": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        # 개인 일정 가져오기
        schedules = PersonalSchedule.objects.filter(user=request.user, date=date_obj)
        schedule_serializer = PersonalScheduleSerializer(schedules, many=True)

        # 루틴 가져오기
        user_routines = UserRoutine.objects.filter(user=request.user, start_date__lte=date_obj, end_date__gte=date_obj)
        routine_serializer = UserRoutineSerializer(user_routines, many=True, context={'request': request, 'selected_date': date_obj})

        data = {
                'schedules': schedule_serializer.data,
                'routines': routine_serializer.data
            }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_schedule(self, request, date=None):
        date_obj = parse_date(date)
        if not date_obj:
            return Response({"detail": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['user'] = request.user.id
        data['date'] = date_obj

        serializer = PersonalScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'])
    def update_schedule(self, request, date=None):
        # 날짜 파싱
        date_obj = parse_date(date)
        if not date_obj:
            return Response({"detail": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        # 요청 본문에서 필수 ID와 선택적 필드 가져오기
        schedule_id = request.data.get('id')
        if not schedule_id:
            return Response({"detail": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 날짜와 사용자에 대한 PersonalSchedule 필터링
        schedules = PersonalSchedule.objects.filter(user=request.user, date=date_obj)

        # ID에 해당하는 스케줄 찾기
        try:
            schedule = schedules.get(id=schedule_id)
        except PersonalSchedule.DoesNotExist:
            return Response({"detail": "PersonalSchedule not found"}, status=status.HTTP_404_NOT_FOUND)

        # 업데이트할 데이터 준비
        updated_data = {}
        if 'title' in request.data:
            updated_data['title'] = request.data['title']
        if 'description' in request.data:
            updated_data['description'] = request.data['description']
        if 'completed' in request.data:
            updated_data['completed'] = request.data['completed']

        # Serializer를 사용하여 데이터 검증 및 저장
        serializer = PersonalScheduleSerializer(schedule, data=updated_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=True, methods=['post'])
    def add_routine(self, request, id=None):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            routine = Routine.objects.get(id=id)
        except Routine.DoesNotExist:
            return Response({'error': 'Routine not found'}, status=status.HTTP_404_NOT_FOUND)

        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')

        if not start_date_str or not end_date_str:
            return Response({'error': 'Start date and end date are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
            if start_date is None or end_date is None:
                raise ValueError("Invalid date format")
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        if start_date > end_date:
            return Response({'error': 'End date must be after start date.'}, status=status.HTTP_400_BAD_REQUEST)

        if end_date < date.today():
            return Response({'error': 'End date cannot be in the past.'}, status=status.HTTP_400_BAD_REQUEST)

        # 동일한 날짜에 동일한 루틴이 이미 존재하는지 확인
        existing_routine = UserRoutine.objects.filter(
            user=user,
            routine=routine,
            start_date__lte=start_date,
            end_date__gte=start_date
        ).exists()

        if existing_routine:
            return Response({'error': 'A routine with the same dates already exists for this user on this date.'}, status=status.HTTP_400_BAD_REQUEST)

        user_routine = UserRoutine.objects.create(
            user=user,
            routine=routine,
            start_date=start_date,
            end_date=end_date
        )

        response_data = {
            'id': routine.id,
            'status': status.HTTP_201_CREATED
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
    # # 루틴과 스케쥴에 대해서 완료된 날짜만 리스트 반환 / 문제: 스케쥴만 있을 때 반영되지 않음 (필터링 순서 때문에)
    # def check_star(self, request, month=None):
    #     user = self.get_user(request)

    #     if user is None:
    #         return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

    #     if not month:
    #         return Response({'error': 'Month parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # 월을 'YYYY-MM' 형식으로 파싱
    #         year, month = month.split('-')
    #         year = int(year)
    #         month = int(month)
    #         if month < 1 or month > 12:
    #             raise ValueError("Invalid month")
            
    #         start_date = datetime(year, month, 1)
    #         end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    #     except (ValueError, TypeError):
    #         return Response({'error': 'Invalid month format'}, status=status.HTTP_400_BAD_REQUEST)

    #     # 해당 월의 모든 루틴을 가져옴
    #     user_routines = UserRoutine.objects.filter(
    #         user=user,
    #         start_date__lte=end_date,
    #         end_date__gte=start_date
    #     )

    #     # 해당 월의 모든 스케줄을 가져옴
    #     personal_schedules = PersonalSchedule.objects.filter(
    #         user=user,
    #         date__range=[start_date, end_date],
    #         completed=True
    #     )

    #     # 루틴이 완료된 날짜를 수집
    #     completed_dates = defaultdict(set)
    #     for user_routine in user_routines:
    #         routine_completed_dates = UserRoutineCompletion.objects.filter(
    #             user=user,
    #             routine=user_routine,
    #             date__range=[start_date, end_date],
    #             completed=True
    #         ).values_list('date', flat=True)
    #         for date in routine_completed_dates:
    #             completed_dates[date].add(user_routine.id)

    #     # 모든 루틴이 완료된 날짜 필터링
    #     all_routines_count = user_routines.count()
    #     fully_completed_routine_dates = [
    #         date for date, items in completed_dates.items()
    #         if len(items) == all_routines_count
    #     ]

    #     # 스케줄이 완료된 날짜를 수집
    #     schedule_completed_dates = set(personal_schedules.values_list('date', flat=True))

    #     # 루틴과 스케줄이 모두 완료된 날짜 필터링
    #     fully_completed_dates = [
    #         date for date in fully_completed_routine_dates
    #         if date in schedule_completed_dates
    #     ]

    #     # 결과를 문자열 형식으로 변환
    #     completed_days = sorted(date.strftime('%Y-%m-%d') for date in fully_completed_dates)

    #     response_data = {
    #         'completed_days': completed_days
    #     }

    #     return Response(response_data, status=status.HTTP_200_OK)

    # 중복으로 뜸 / 루틴이 완료 안되어도 스케쥴이 완료이면 반환
    # @action(detail=False, methods=['get'])
    # def check_star(self, request, month=None):
    #     user = self.get_user(request)

    #     if user is None:
    #         return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

    #     if not month:
    #         return Response({'error': 'Month parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # 월을 'YYYY-MM' 형식으로 파싱
    #         year, month = month.split('-')
    #         year = int(year)
    #         month = int(month)
    #         if month < 1 or month > 12:
    #             raise ValueError("Invalid month")
            
    #         start_date = datetime(year, month, 1)
    #         end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    #     except (ValueError, TypeError):
    #         return Response({'error': 'Invalid month format'}, status=status.HTTP_400_BAD_REQUEST)

    #     # 해당 월의 모든 루틴을 가져옴
    #     user_routines = UserRoutine.objects.filter(
    #         user=user,
    #         start_date__lte=end_date,
    #         end_date__gte=start_date
    #     )

    #     # 해당 월의 모든 스케줄을 가져옴
    #     personal_schedules = PersonalSchedule.objects.filter(
    #         user=user,
    #         date__range=[start_date, end_date]
    #     )

    #     # 루틴이 완료된 날짜를 수집
    #     completed_dates = defaultdict(set)
    #     for user_routine in user_routines:
    #         routine_completed_dates = UserRoutineCompletion.objects.filter(
    #             user=user,
    #             routine=user_routine,
    #             date__range=[start_date, end_date],
    #             completed=True
    #         ).values_list('date', flat=True)
    #         for date in routine_completed_dates:
    #             completed_dates[date].add(user_routine.id)

    #     all_routines_count = user_routines.count()
    #     fully_completed_routine_dates = [
    #         date for date, items in completed_dates.items()
    #         if len(items) == all_routines_count
    #     ]

    #     # 스케줄이 완료된 날짜를 수집
    #     schedule_completed_dates = set(personal_schedules.filter(completed=True).values_list('date', flat=True))
    #     all_schedules_dates = set(personal_schedules.values_list('date', flat=True))

    #     # 루틴과 스케줄 모두 완료된 날짜 필터링
    #     fully_completed_dates = [
    #         date for date in fully_completed_routine_dates
    #         if date in schedule_completed_dates
    #     ]

    #     # 스케줄만 있는 날짜에 대해 스케줄이 모두 완료된 경우를 확인
    #     fully_completed_schedule_dates = [
    #         date for date in all_schedules_dates
    #         if personal_schedules.filter(date=date).filter(completed=True).count() == personal_schedules.filter(date=date).count()
    #     ]

    #     # 결과를 문자열 형식으로 변환
    #     completed_days = sorted(
    #         date.strftime('%Y-%m-%d')
    #         for date in (fully_completed_dates + fully_completed_schedule_dates)
    #     )

    #     response_data = {
    #         'completed_days': completed_days
    #     }

    #     return Response(response_data, status=status.HTTP_200_OK)

    # #중복으로 반환되는 문제는 해결
    # #루틴이 완료안됐는데 스케쥴이 완료니까 이 날짜 반환
    # #그리고 루틴이 2개 이상인 날짜에서, 두개 다 완료인데, 이 날짜가 반환되지 않음
    # @action(detail=False, methods=['get'])
    # def check_star(self, request, month=None):
    #     user = self.get_user(request)

    #     if user is None:
    #         return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

    #     if not month:
    #         return Response({'error': 'Month parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # 월을 'YYYY-MM' 형식으로 파싱
    #         year, month = month.split('-')
    #         year = int(year)
    #         month = int(month)
    #         if month < 1 or month > 12:
    #             raise ValueError("Invalid month")
            
    #         start_date = datetime(year, month, 1)
    #         end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    #     except (ValueError, TypeError):
    #         return Response({'error': 'Invalid month format'}, status=status.HTTP_400_BAD_REQUEST)

    #     # 해당 월의 모든 루틴을 가져옴
    #     user_routines = UserRoutine.objects.filter(
    #         user=user,
    #         start_date__lte=end_date,
    #         end_date__gte=start_date
    #     )

    #     # 해당 월의 모든 스케줄을 가져옴
    #     personal_schedules = PersonalSchedule.objects.filter(
    #         user=user,
    #         date__range=[start_date, end_date]
    #     )

    #     # 루틴이 완료된 날짜를 수집
    #     completed_dates = defaultdict(set)
    #     for user_routine in user_routines:
    #         routine_completed_dates = UserRoutineCompletion.objects.filter(
    #             user=user,
    #             routine=user_routine,
    #             date__range=[start_date, end_date],
    #             completed=True
    #         ).values_list('date', flat=True)
    #         for date in routine_completed_dates:
    #             completed_dates[date].add(user_routine.id)

    #     all_routines_count = user_routines.count()
    #     fully_completed_routine_dates = [
    #         date for date, items in completed_dates.items()
    #         if len(items) == all_routines_count
    #     ]

    #     # 스케줄이 완료된 날짜를 수집
    #     schedule_completed_dates = set(personal_schedules.filter(completed=True).values_list('date', flat=True))
    #     all_schedules_dates = set(personal_schedules.values_list('date', flat=True))

    #     # 루틴과 스케줄 모두 완료된 날짜 필터링
    #     fully_completed_dates = set(
    #         date for date in fully_completed_routine_dates
    #         if date in schedule_completed_dates
    #     )

    #     # 스케줄만 있는 날짜에서 모든 스케줄이 완료된 날짜 필터링
    #     fully_completed_schedule_dates = set(
    #         date for date in all_schedules_dates
    #         if personal_schedules.filter(date=date).filter(completed=True).count() == personal_schedules.filter(date=date).count()
    #     )

    #     # 루틴과 스케줄 모두 완료된 날짜와 스케줄만 완료된 날짜를 합집합으로 구함
    #     completed_dates_combined = fully_completed_dates.union(fully_completed_schedule_dates)

    #     # 결과를 문자열 형식으로 변환
    #     completed_days = sorted(
    #         date.strftime('%Y-%m-%d')
    #         for date in completed_dates_combined
    #     )

    #     response_data = {
    #         'completed_days': completed_days
    #     }

    #     return Response(response_data, status=status.HTTP_200_OK)
    
    ##
    @action(detail=False, methods=['get'])
    def check_star(self, request, month=None):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        if not month:
            return Response({'error': 'Month parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 월을 'YYYY-MM' 형식으로 파싱하여 시작일과 종료일을 계산합니다
            year, month = month.split('-')
            year = int(year)
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError("Invalid month")

            start_date = datetime(year, month, 1)  # 월의 첫째 날
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)  # 월의 마지막 날
        except (ValueError, TypeError):
            return Response({'error': 'Invalid month format'}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 월의 모든 루틴을 가져옵니다
        user_routines = UserRoutine.objects.filter(
            user=user,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        # 해당 월의 모든 스케줄을 가져옵니다 (완료된 것만)
        personal_schedules = PersonalSchedule.objects.filter(
            user=user,
            date__range=[start_date, end_date],
            completed=True
        )

        # 루틴이 완료된 날짜를 수집합니다
        completed_dates = defaultdict(set)
        for user_routine in user_routines:
            routine_completed_dates = UserRoutineCompletion.objects.filter(
                user=user,
                routine=user_routine,
                date__range=[start_date, end_date],
                completed=True
            ).values_list('date', flat=True)
            for date in routine_completed_dates:
                completed_dates[date].add(user_routine.id)

        # 모든 루틴이 완료된 날짜를 필터링합니다
        all_routines_count = user_routines.count()
        fully_completed_routine_dates = [
            date for date, items in completed_dates.items()
            if len(items) == all_routines_count
        ]

        # 스케줄이 완료된 날짜를 수집합니다
        schedule_completed_dates = set(personal_schedules.values_list('date', flat=True))

        # 루틴과 스케줄이 모두 완료된 날짜를 필터링합니다
        fully_completed_dates = [
            date for date in fully_completed_routine_dates
            if date in schedule_completed_dates
        ]

        # 결과를 문자열 형식으로 변환합니다
        completed_days = sorted(date.strftime('%Y-%m-%d') for date in fully_completed_dates)

        response_data = {
            'completed_days': completed_days
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
class UpdateRoutineCompletionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, date):
        try:
            user = request.user
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            routine_id = request.data.get('routine_id')
            completed = request.data.get('completed')

            if routine_id is None or completed is None:
                return Response({"detail": "Missing routine_id or completed field."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                completion = UserRoutineCompletion.objects.get(user=user, routine_id=routine_id, date=date_obj)
                completion.completed = completed
                completion.save()
            except UserRoutineCompletion.DoesNotExist:
                return Response({"detail": "UserRoutineCompletion not found."}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({"status": "Routine completion status updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)