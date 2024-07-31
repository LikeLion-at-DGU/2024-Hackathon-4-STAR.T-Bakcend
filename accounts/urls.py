# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (
    GoogleLoginView,
    KakaoLoginView,
    NaverLoginView,
    UserViewSet,
    CustomRoutineView,
    UpdateNicknameView,
)

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth.registration/',include('dj_rest_auth.registration.urls')),

    path('kakao/login/', KakaoLoginView.as_view(), name='api_accounts_kakao_oauth'),
    path('google/login/', GoogleLoginView.as_view(), name='api_accounts_google_oauth'),
    path('naver/login/', NaverLoginView.as_view(), name='api_accounts_naver_oauth'),
    path('custom-routines/', CustomRoutineView.as_view(), name='custom-routines'),
    path('info/', UpdateNicknameView.as_view(), name='update_nickname'),
    
    path('', include(router.urls)),
]
