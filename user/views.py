from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer

# 사용자 목록 조회 및 생성 뷰
class UserListCreateView(generics.ListCreateAPIView):
    # 조회할 쿼리셋 설정
    queryset = User.objects.all()
    # 사용할 직렬화기 설정
    serializer_class = UserSerializer
    # 접근 권한 설정 (인증된 사용자만 접근 가능)
    permission_classes = [IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
