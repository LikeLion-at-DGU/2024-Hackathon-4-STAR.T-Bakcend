from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarViewSet, UpdateRoutineCompletionView

router = DefaultRouter()
router.register(r'calendar', CalendarViewSet, basename='calendar')

urlpatterns = [
    path('', include(router.urls)),
    path('calendar/daily/<str:date>/', CalendarViewSet.as_view({'get': 'daily', 'post': 'create_schedule', 'patch': 'update_schedule'}), name='calendar-daily'),
    path('calendar/daily/<str:date>/delete/<int:id>/', CalendarViewSet.as_view({'delete': 'delete_daily'}), name='calendar-daily-personalschedule-delete'),
    path('add_routine/<int:id>/', CalendarViewSet.as_view({'post': 'add_routine'}), name='add-routine'),
    path('calendar/check_star/<str:month>/', CalendarViewSet.as_view({'get': 'check_star'}), name='check_star'),
    path('calendar/daily/<str:date>/update_routine/', UpdateRoutineCompletionView.as_view(), name='update-routine'),
    # path('completed-dates/<int:year>/<int:month>/', CompletedDatesView.as_view(), name='completed-dates'),
    ]
