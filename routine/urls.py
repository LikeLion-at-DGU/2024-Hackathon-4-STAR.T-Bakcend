from django.urls import path, include
from .views import RoutineViewSet
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

app_name = 'routine'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register(r'routine', RoutineViewSet, basename='routine')
urlpatterns = [
    path('', include(default_router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
