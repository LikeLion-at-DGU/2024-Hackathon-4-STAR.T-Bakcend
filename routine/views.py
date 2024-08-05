from rest_framework import viewsets,mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import RoutineSerializer,RoutineCategorySerializer , RoutineDiceSerializer
from search.serializers import ThemeSerializer
from .models import Routine , RoutineCategory
from search.models import Theme
from rest_framework.decorators import action
from calen.models import UserRoutine
from calen.serializers import UserRoutineSerializer
from accounts.models import User
from accounts.serializers import NicknameSerializer
import random
from django.db.models import F, Subquery

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def recommend(self, request):
        ran_routine = self.get_queryset().order_by("?").first()
        if not ran_routine:
            return Response({"detail": "No routines available"}, status=404)
        
        ran_routine_serializer = RoutineDiceSerializer(ran_routine)
        return Response(ran_routine_serializer.data)
    

class MainPageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        user_routines = []  # 초기화 # 유저 인증 해결 되면 반환 됨
        
        if user.is_authenticated:
            user_categories = user.preferred_routine_categories.all()
            if user_categories.exists():
                user_routines = Routine.objects.filter(category__in=user_categories).distinct()
            else:
                user_routines = Routine.objects.all().order_by("?")[:10]
                print("유저가 선택한 맞춤형 루틴이 없습니다!!!!!")
        else:
            print("유저가 선택한 맞춤형 루틴이 없습니다!!!!!")  # 일단 무작위
            user_routines = Routine.objects.all().order_by("?")[:10]
            
        hot_routines = Routine.objects.order_by('-popular')[:10]
        latest_routines = Routine.objects.order_by('-create_at')[:10]
        themes = Theme.objects.all()

        challenge_set = UserRoutine.objects.filter(user=user)
        challenge_set = challenge_set.annotate(routine_id=F('routine_id'))
        challenge_set = challenge_set.values('routine_id').distinct()

        subquery = UserRoutine.objects.filter(
            id__in=Subquery(
                challenge_set.values('id')
            )
        )

        challenges = subquery.distinct()
        challenge_data = []
        for challenge in challenges:
            routine = challenge.routine
            routine_data = {
                "id": routine.id,
                "title": routine.title,
                "celeb_name": routine.celebrity.name,
                "image": routine.image,  # 이미지 URL로 가정
                "url": routine.celebrity.id,  # Celeb 페이지 URL로 가정
                "start_date": challenge.start_date,
                "end_date": challenge.end_date
            }
            challenge_data.append(routine_data)

        theme_data = []
        for theme in themes:
            theme_data.append({
                "id": theme.id,
                "title": theme.title,
                "routine_title": [theme.sub_title],
                "image": theme.image,
                "url": theme.id
            })

        def create_routine_data(routines, include_popular=False):
            routine_data = []
            for routine in routines:
                # routine.celebrity가 유효한 Celebrity 객체인지 확인
                if not hasattr(routine.celebrity, 'id'):
                    continue  # celebrity가 유효하지 않으면 무시
                routine_info = {
                    "id": routine.id,
                    "title": routine.title,
                    "celeb_name": routine.celebrity.name,
                    "image": routine.image,
                    "create_at": routine.create_at,  # 추가된 필드
                    "url": routine.celebrity.id  # Celeb 페이지 URL
                }
                if include_popular:
                    routine_info["popular"] = routine.popular
                routine_data.append(routine_info)
            return routine_data
        
        new_update_data = create_routine_data(latest_routines)
        user_routine_data = create_routine_data(user_routines)
        hot_routine_data = create_routine_data(hot_routines)

        random.shuffle(new_update_data)
        random.shuffle(user_routine_data)
        random.shuffle(hot_routine_data)
        random.shuffle(challenge_data)


        return Response({
            "theme": theme_data,
            "도전중인 챌린지" : challenge_data,
            "최근 업데이트": new_update_data,
            f"{user.nickname}님을 위한 맞춤형 루틴": user_routine_data,
            "주간 HOT 루틴": hot_routine_data
        })


            