from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarViewSet, UpdateRoutineCompletionView, UpdateScheduleView

router = DefaultRouter()
router.register(r'calendar', CalendarViewSet, basename='calendar')

urlpatterns = [
    path('', include(router.urls)),
    path('calendar/monthly/<str:month>/', CalendarViewSet.as_view({'get': 'monthly', 'post':'monthly', 'patch':'monthly'}), name='calendar-monthly'),
    path('calendar/daily/<str:date>/', CalendarViewSet.as_view({'get': 'daily', 'post': 'daily'}), name='calendar-daily'),
    path('calendar/daily/<str:date>/delete/<int:id>/', CalendarViewSet.as_view({'delete': 'delete_daily'}), name='calendar-daily-personalschedule-delete'),
    path('add_routine/<int:id>/', CalendarViewSet.as_view({'post': 'add_routine'}), name='add-routine'),
    path('calendar/check_star/<str:date>/', CalendarViewSet.as_view({'get': 'check_star'}), name='check_star'),
    # path('calendar/daily/<str:date>/update_routine/', CalendarViewSet.as_view({'patch': 'update_routine'}), name='update-routine'),
    # path('calendar/daily/<str:date>/update_schedule/', CalendarViewSet.as_view({'patch': 'update_schedule'}), name='update-schedule'),
    path('calendar/daily/<str:date>/update_routine/', UpdateRoutineCompletionView.as_view(), name='update-routine'),
    path('calendar/daily/<str:date>/update_schedule/', UpdateScheduleView.as_view(), name='update-schedule'),
]
