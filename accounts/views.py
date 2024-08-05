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
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets,generics
from rest_framework.views import APIView
from .serializers import CustomRoutineSerializer,UserSerializer,NicknameSerializer ,UserProfileSerializer
from .models import User
from rank.models import CelebScore
from rank.serializers import CelebScoreSerializer
from routine.serializers import RoutineCategorySerializer
from django.core.exceptions import ObjectDoesNotExist



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
    try:
        user = User.objects.get(email=email_address)
    except ObjectDoesNotExist:
        user = User.objects.create(email=email_address, username=email_address.split('@')[0])
        user.save()

    perform_login(request, user, email_verification='optional')

    refresh = RefreshToken.for_user(user)
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
    # else:
    # # Here, the user is not registered yet. We handle the pre-signup logic.
    # # You might want to redirect to a page where the user can complete the registration.
    #     temp_user = sociallogin.user
    #     request.session['socialaccount_sociallogin'] = sociallogin.serialize()

    #     response = redirect('https://www.likelion-start.site/signup')  # Change this to your actual signup completion URL
    #     raise ImmediateHttpResponse(response)
    

def home(request):
    return render(request, 'home.html')

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  #IsAuthenticated

    def list(self, request):
        user = request.user
    # if not user.is_authenticated:
    #    return Response({'error': 'User not authenticated'}, status=401)
        
        users = User.objects.filter(email=user.email)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    


class CustomRoutineView(APIView):
    permission_classes = [AllowAny]  # 모든 사용자에게 접근 허용

    def get(self, request):
        if not request.user.is_authenticated: #인증
            return Response({"message": "인증 되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        preferred_routine_categories = user.preferred_routine_categories.all()
        serializer = RoutineCategorySerializer(preferred_routine_categories, many=True)
        if serializer.is_valid:
            return Response({
                "status": 200,
                "preferred_routine_categories": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User prefer routine categories do not exist."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 디버깅을 위한 요청 데이터 로깅
        print("요청 데이터 : ", request.data)  # 프로덕션 환경에서는 적절한 로깅으로 대체하세요.

        serializer = CustomRoutineSerializer(data=request.data)
        if serializer.is_valid():
            preferred_routine_categories = serializer.validated_data['preferred_routine_categories']
            user = request.user  # 현재 사용자 가져오기
            
            #사용자가 올바르게 인증되었는지 확인
            if not user:
                return Response({"message": "No user available for testing."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # 사용자의 선호 카테고리 업데이트
                user.preferred_routine_categories.set(preferred_routine_categories)
                user.save()

                return Response({
                    "status": 200,
                    "message": "Preferred routine categories updated successfully."
                }, status=status.HTTP_200_OK)

            except Exception as e:
                # 업데이트 중 발생한 예외를 로깅
                print("Error updating user preferences:", str(e))
                return Response({
                    "status": 500,
                    "message": "An error occurred while updating preferences."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Serializer 에러 로깅
            print("시리얼라이저 에러", serializer.errors)  # 프로덕션 환경에서는 적절한 로깅으로 대체하세요.
            return Response({
                "status": 400,
                "message": serializer.errors  # 에러 메시지 반환
            }, status=status.HTTP_400_BAD_REQUEST)
    

        
    def patch(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CustomRoutineSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            preferred_routine_categories = serializer.validated_data['preferred_routine_categories']
            user = request.user
            user.preferred_routine_categories.clear() # 기존 값들 제거
            for category in preferred_routine_categories:
                if not user.preferred_routine_categories.filter(id=category.id).exists():
                    user.preferred_routine_categories.add(category)
            user.save()
            return Response({
                "status": 200,
                "message": "Preferred routine categories updated successfully."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 400,
                "message": "Preferred routine categories are required."
            }, status=status.HTTP_400_BAD_REQUEST)

    ## 선호 루틴 삭제
    # def delete(self, request):
    # if not request.user.is_authenticated:
    #         return Response({"message": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    
    #     user = request.user
    #     user.preferred_routine_categories.clear()
    #     user.save()
    #     return Response({
    #         "status": 200,
    #         "message": "Preferred routine categories cleared successfully."
    #     }, status=status.HTTP_200_OK)


class UpdateNicknameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = NicknameSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            user.nickname = serializer.validated_data['nickname']
            user.save()
            return Response({"status": 200, "message": "정상적으로 등록되었습니다."}, status=status.HTTP_200_OK)
        
        return Response({"status": 400, "message": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

# class UpdateNicknameView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = NicknameSerializer(data=request.data)

#         if serializer.is_valid():
#             user = request.user
#             user.nickname = serializer.validated_data['nickname']
#             user.save()

#             # JWT 토큰 생성
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             refresh_token = str(refresh)

#             response = Response({"status": 200, "message": "정상적으로 등록되었습니다."}, status=status.HTTP_200_OK)
            
#             # 쿠키에 토큰 설정
#             response.set_cookie(
#             key='access_token',
#             value=access_token,
#             domain='likelion-start.site',
#             httponly=True,
#             secure=False,
#             samesite='Lax'
#             )
#             response.set_cookie(
#             key='refresh_token',
#             value=refresh_token,
#             domain='likelion-start.site',
#             httponly=True,
#             secure=False,
#             samesite='Lax'
#             )

#             return response

#         return Response({"status": 400, "message": "닉네임을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)





# 사용자 프로필 정보를 가져오는 뷰
class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()  # 모든 사용자를 쿼리셋으로 설정 (실제 사용자는 get_object 메서드를 통해 얻음)
    serializer_class = UserProfileSerializer  # 사용할 Serializer 지정
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_object(self):
        # 현재 인증된 사용자를 반환하는 메서드
        return self.request.user  # 요청한 사용자 객체를 반환

    def get_serializer_context(self):
        # request 객체를 context에 추가
        context = super().get_serializer_context()
        context['request'] = self.request
        return context