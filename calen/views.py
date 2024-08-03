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

class CalendarViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        user = request.user
        if not user.is_authenticated:
            return None
        return user
    
    # 기존 mothly 코드
    @action(detail=False, methods=['get', 'post', 'patch'])
    def monthly(self, request, month=None):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        if not month:
            return Response({'error': 'Month parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 요청된 월을 파싱하여 년과 월을 추출
            month_date = parse_date(month + "-01")
            if month_date is None:
                raise ValueError("Invalid month format")

            year = month_date.year
            month = month_date.month

            if request.method == 'GET':
                completed_routines = UserRoutineCompletion.objects.filter(
                    user=user,
                    date__year=year,
                    date__month=month,
                    completed=True
                )

                # completed_days 리스트 생성
                completed_days = set()

                for routine_completion in completed_routines:
                    completed_days.add(routine_completion.date)

                monthly_title = MonthlyTitle.objects.filter(
                    user=user,
                    month__year=year,
                    month__month=month
                )            

                return Response({
                    'completed_days': [day.strftime('%Y-%m-%d') for day in sorted(completed_days)],
                    'monthly_title': MonthlyTitleSerializer(monthly_title, many=True).data
                })

            elif request.method == 'POST':
                if MonthlyTitle.objects.filter(user=user, month__year=year, month__month=month).exists():
                    return Response({'error': 'MonthlyTitle for this month already exists.'}, status=status.HTTP_400_BAD_REQUEST)

                serializer = MonthlyTitleSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=user, month=month_date)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            elif request.method == 'PATCH':
                title_id = request.data.get('id')
                if not title_id:
                    return Response({'error': 'ID parameter is required for update'}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    monthly_title = MonthlyTitle.objects.get(id=title_id, user=user, month__year=year, month__month=month)
                except MonthlyTitle.DoesNotExist:
                    return Response({'error': 'MonthlyTitle not found'}, status=status.HTTP_404_NOT_FOUND)

                serializer = MonthlyTitleSerializer(monthly_title, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # comleted days 반환값 수정중인 코드(현재 버그 있을)
    # @action(detail=False, methods=['get', 'post', 'patch'])
    # def monthly(self, request, month=None):
    #     user = self.get_user(request)

    #     if user is None:
    #         return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

    #     if not month:
    #         return Response({'error': 'Month parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         # 요청된 월을 파싱하여 년과 월을 추출
    #         month_date = parse_date(month + "-01")
    #         if month_date is None:
    #             raise ValueError("Invalid month format")

    #         year = month_date.year
    #         month = month_date.month

    #         if request.method == 'GET':
    #             completed_days = set()
                
    #             # 해당 월의 모든 날짜를 순회
    #             first_day = date(year, month, 1)
    #             last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    #             current_date = first_day
    #             while current_date <= last_day:
    #                 # 해당 날짜의 모든 루틴을 가져옴
    #                 user_routines = UserRoutine.objects.filter(
    #                     user=user,
    #                     start_date__lte=current_date,
    #                     end_date__gte=current_date
    #                 )

    #                 # 모든 루틴이 완료되었는지 확인
    #                 all_completed = all(UserRoutineCompletion.objects.filter(
    #                     user=user,
    #                     routine=user_routine,
    #                     date=current_date,
    #                     completed=True
    #                 ).exists() for user_routine in user_routines)

    #                 if all_completed:
    #                     completed_days.add(current_date)

    #                 current_date += timedelta(days=1)

    #             monthly_title = MonthlyTitle.objects.filter(
    #                 user=user,
    #                 month__year=year,
    #                 month__month=month
    #             )            

    #             return Response({
    #                 'completed_days': [day.strftime('%Y-%m-%d') for day in sorted(completed_days)],
    #                 'monthly_title': MonthlyTitleSerializer(monthly_title, many=True).data
    #             })

    #         elif request.method == 'POST':
    #             if MonthlyTitle.objects.filter(user=user, month__year=year, month__month=month).exists():
    #                 return Response({'error': 'MonthlyTitle for this month already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    #             serializer = MonthlyTitleSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 serializer.save(user=user, month=month_date)
    #                 return Response(serializer.data, status=status.HTTP_201_CREATED)
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    #         elif request.method == 'PATCH':
    #             title_id = request.data.get('id')
    #             if not title_id:
    #                 return Response({'error': 'ID parameter is required for update'}, status=status.HTTP_400_BAD_REQUEST)
                
    #             try:
    #                 monthly_title = MonthlyTitle.objects.get(id=title_id, user=user, month__year=year, month__month=month)
    #             except MonthlyTitle.DoesNotExist:
    #                 return Response({'error': 'MonthlyTitle not found'}, status=status.HTTP_404_NOT_FOUND)

    #             serializer = MonthlyTitleSerializer(monthly_title, data=request.data, partial=True)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 return Response(serializer.data, status=status.HTTP_200_OK)
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    #     except ValueError as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)        
    
    @action(detail=False, methods=['get', 'post'])
    def daily(self, request, date=None):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        if not date:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_date = parse_date(date)
            if selected_date is None:
                raise ValueError("Invalid date format")
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            routines = UserRoutine.objects.filter(
                user=user,
                start_date__lte=selected_date,
                end_date__gte=selected_date,
            )
            schedules = PersonalSchedule.objects.filter(
                user=user,
                date=selected_date
            )

            serializer_context = {
                'request': request,
                'selected_date': selected_date
            }

            return Response({
                'date': selected_date.strftime('%Y-%m-%d'),
                'routines': UserRoutineSerializer(routines, many=True, context=serializer_context).data,
                'schedules': PersonalScheduleSerializer(schedules, many=True).data,
            })

        elif request.method == 'POST':
            serializer = PersonalScheduleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user, date=selected_date)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PATCH':
            try:
                schedule_id = request.data.get('id')
                schedule = PersonalSchedule.objects.get(id=schedule_id, user=user)
            except PersonalSchedule.DoesNotExist:
                return Response({'error': 'PersonalSchedule not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = PersonalScheduleSerializer(schedule, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=False, methods=['delete'])
    def delete_daily(self, request, date=None, id=None):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        if not date or not id:
            return Response({'error': 'Date and ID parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_date = parse_date(date)
            if selected_date is None:
                raise ValueError("Invalid date format")

            # 특정 ID와 날짜로 PersonalSchedule 객체를 찾기
            schedule = PersonalSchedule.objects.get(id=id, user=user, date=selected_date)
            schedule.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PersonalSchedule.DoesNotExist:
            return Response({'error': 'PersonalSchedule not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        
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

        # 동일한 날짜와 루틴이 이미 존재하는지 확인
        existing_routine = UserRoutine.objects.filter(
            user=user,
            routine=routine,
            start_date=start_date,
            end_date=end_date
        ).exists()

        if existing_routine:
            return Response({'error': 'A routine with the same dates already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

        user_routine = UserRoutine.objects.create(
            user=user,
            routine=routine,
            start_date=start_date,
            end_date=end_date
        )

        # routine.popular += 1
        # routine.save()

        # 반환 데이터 수정 전
        # serializer = UserRoutineSerializer(user_routine, context={'request': request})
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        response_data = {
        'id': routine.id,
        'status': status.HTTP_201_CREATED
    }

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def check_star(self, request):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        date_str = request.data.get('date')
        if not date_str:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_date = parse_date(date_str)
        except (ValueError, TypeError, OverflowError, ValidationError):
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # 해당 날짜의 모든 루틴을 가져옴
        user_routines = UserRoutine.objects.filter(
            user=user,
            start_date__lte=selected_date,
            end_date__gte=selected_date
        )

        # 모든 루틴이 완료되었는지 확인
        all_completed = all(UserRoutineCompletion.objects.filter(
            user=user,
            routine=user_routine,
            date=selected_date,
            completed=True
        ).exists() for user_routine in user_routines)

        return Response({'check_star': all_completed}, status=status.HTTP_200_OK)

    # 루틴 complete 업데이트
    @action(detail=False, methods=['patch'])
    def update_routine(self, request, date=None):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        if not date:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_date = parse_date(date)
            if selected_date is None:
                raise ValueError("Invalid date format")
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        routines_data = request.data.get('routines', [])

        for routine_data in routines_data:
            routine_id = routine_data.get('id')
            completed = routine_data.get('completed')

            if routine_id is None or completed is None:
                return Response({'error': 'Routine ID and completion status are required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                routine = UserRoutine.objects.get(id=routine_id, user=user, start_date__lte=selected_date, end_date__gte=selected_date)
            except UserRoutine.DoesNotExist:
                return Response({'error': 'Routine not found or does not belong to the user.'}, status=status.HTTP_404_NOT_FOUND)

            UserRoutineCompletion.objects.update_or_create(
                user=user,
                routine=routine,
                date=selected_date,
                defaults={'completed': completed}
            )

        return Response({'status': 'Routines updated successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['patch'])
    def update_schedule(self, request, date=None):
        user = self.get_user(request)

        if user is None:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        if not date:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_date = parse_date(date)
            if selected_date is None:
                raise ValueError("Invalid date format")
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        schedules_data = request.data.get('schedules', [])

        for schedule_data in schedules_data:
            schedule_id = schedule_data.get('id')
            if schedule_id:
                try:
                    schedule = PersonalSchedule.objects.get(id=schedule_id, user=user, date=selected_date)
                except PersonalSchedule.DoesNotExist:
                    return Response({'error': 'PersonalSchedule not found'}, status=status.HTTP_404_NOT_FOUND)

                serializer = PersonalScheduleSerializer(schedule, data=schedule_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'Schedules updated successfully'}, status=status.HTTP_200_OK)