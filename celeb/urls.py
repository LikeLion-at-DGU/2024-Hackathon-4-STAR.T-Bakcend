from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CelebViewSet

router = DefaultRouter()
router.register(r'celeb', CelebViewSet)

urlpatterns = [
    path('', include(router.urls)),
]