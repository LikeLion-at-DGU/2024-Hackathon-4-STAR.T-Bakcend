from django.urls import path, include
from .views import SearchViewSet,ThemeDetailViewSet
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

app_name = 'search'

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register(r'search', SearchViewSet, basename='search')
default_router.register(r'theme', ThemeDetailViewSet, basename='theme-detail')

urlpatterns = [
    path('', include(default_router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
