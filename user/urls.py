from django.urls import path
from .views import UserListCreateView, UserDetailView

app_name = 'user'
##일단 초기 세팅
urlpatterns = [
        # 사용자 목록 조회 및 생성 엔드포인트
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    # 사용자 상세 조회, 수정, 삭제 엔드포인트
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

]