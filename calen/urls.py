from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarViewSet

router = DefaultRouter()
router.register(r'calendar', CalendarViewSet, basename='calendar')

urlpatterns = [
    path('', include(router.urls)),
    path('calendar/monthly/<str:month>/', CalendarViewSet.as_view({'get': 'monthly'}), name='calendar-monthly'),
    path('calendar/daily/<str:date>', CalendarViewSet.as_view({'get': 'daily', 'post': 'daily', 'patch': 'daily', 'delete': 'daily'}), name='calendar-daily'),
]
