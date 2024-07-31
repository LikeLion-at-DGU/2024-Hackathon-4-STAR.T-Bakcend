# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (
    GoogleLoginView,
    KakaoLoginView,
    NaverLoginView,
    UserViewSet
)

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('kakao/login/', KakaoLoginView.as_view(), name='api_accounts_kakao_oauth'),
    path('google/login/', GoogleLoginView.as_view(), name='api_accounts_google_oauth'),
    path('naver/login/', NaverLoginView.as_view(), name='api_accounts_naver_oauth'),
    path('', include(router.urls)),
]
