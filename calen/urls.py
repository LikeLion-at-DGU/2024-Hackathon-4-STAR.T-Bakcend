from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarViewSet

router = DefaultRouter()
router.register(r'calendar', CalendarViewSet, basename='calendar')

urlpatterns = [
    path('', include(router.urls)),
    path('calendar/monthly/<str:month>/', CalendarViewSet.as_view({'get': 'monthly', 'post':'monthly', 'patch':'monthly'}), name='calendar-monthly'),
    path('calendar/daily/<str:date>/', CalendarViewSet.as_view({'get': 'daily', 'post': 'daily', 'patch': 'daily'}), name='calendar-daily'),
    path('calendar/daily/<str:date>/delete/<int:id>/', CalendarViewSet.as_view({'delete': 'delete_daily'}), name='calendar-daily-personalschedule-delete'),
    path('add_routine/<int:id>/', CalendarViewSet.as_view({'post': 'add_routine'}), name='add-routine'),
]
