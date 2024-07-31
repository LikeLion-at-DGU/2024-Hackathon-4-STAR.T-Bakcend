from django.urls import path, include
from .views import RoutineViewSet, MainPageViewSet
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

app_name = 'routine'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register(r'routine', RoutineViewSet, basename='routine')

main_page_router = routers.SimpleRouter(trailing_slash=False)
main_page_router.register(r'main', MainPageViewSet, basename='main')

urlpatterns = [
    path('', include(default_router.urls)),
    path('', include(main_page_router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
