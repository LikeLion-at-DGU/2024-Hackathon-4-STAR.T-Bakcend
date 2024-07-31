# accounts/views.py
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.dispatch import receiver
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/api/accounts/google/login/callback/'
    client_class = OAuth2Client

class KakaoLoginView(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = 'https://likelion-start.site/api/accounts/kakao/login/callback/'
    client_class = OAuth2Client

class NaverLoginView(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/api/accounts/naver/login/callback/'
    client_class = OAuth2Client

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        pass

PROVIDER_LIST = ['kakao', 'google']

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    provider = sociallogin.account.provider

    if provider == 'kakao':
        email_address = sociallogin.account.extra_data.get('kakao_account').get('email')
    elif provider == 'google':
        email_address = sociallogin.account.extra_data.get('email')
    else:
        print('Provider 없음')
        return

    User = get_user_model()
    users = User.objects.filter(email=email_address)
    if users:
        perform_login(request, users[0], email_verification='optional')

        refresh = RefreshToken.for_user(users[0])
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = redirect(settings.LOGIN_REDIRECT_URL)
        response.set_cookie(
            key='access_token',
            value=access_token,
            domain='likelion-start.site',
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            domain='likelion-start.site',
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        raise ImmediateHttpResponse(response)
    return

def home(request):
    return render(request, 'home.html')

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] 

    def list(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=401)
        
        users = User.objects.filter(email=user.email)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)