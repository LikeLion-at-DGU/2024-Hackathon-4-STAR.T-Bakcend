from rest_framework import viewsets,mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import RoutineSerializer,RoutineCategorySerializer
from search.serializers import ThemeSerializer
from .models import Routine , RoutineCategory
from search.models import Theme
from rest_framework.decorators import action

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    #permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def recommend(self, request):
        ran_routine = self.get_queryset().order_by("?").first()
        if not ran_routine:
            return Response({"detail": "No routines available"}, status=404)
        
        ran_routine_serializer = RoutineSerializer(ran_routine)
        return Response(ran_routine_serializer.data)
    

class MainPageViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        user = request.user
        user_routines = []  # 초기화 # 유저 인증 해결 되면 반환 됨
        # 유저 인증 되면 로직 수정!!
        # if request.user.is_authenticated:
        #     user_categories = user.preferred_routine_categories.all()
        #     if user_categories.exists():
        #         user_routines = Routine.objects.filter(category__in=user_categories).distinct()
        #     else:
        #         user_routines = Routine.objects.all().order_by("?")[:10]
        #         print("유저가 선택한 맞춤형 루틴이 없습니다!!!!!")
        print("유저가 선택한 맞춤형 루틴이 없습니다!!!!!") #일단 무작위
        user_routines = Routine.objects.all().order_by("?")[:10]

        hot_routines = Routine.objects.order_by('-popular')[:10]
        latest_routines = Routine.objects.order_by('-create_at')[:10]
        themes = Theme.objects.all()


        theme_data = []
        for theme in themes:
            routines_serializer = RoutineSerializer(theme.routine_set.all(), many=True)
            theme_data.append({
                "id": theme.id,
                "title": theme.title,
                "routine_title": [routine['title'] for routine in routines_serializer.data],
                "image": theme.image,
                "url": f"https://www.likelion-start.site/api/theme/{theme.id}/"
            })

        def create_routine_data(routines):
            routine_data = []
            for routine in routines:
                # routine.celebrity가 유효한 Celebrity 객체인지 확인
                if not hasattr(routine.celebrity, 'id'):
                    continue  # celebrity가 유효하지 않으면 무시
                routine_data.append({
                    "id": routine.id,
                    "title": routine.title,
                    "celeb_name": routine.celebrity.name,
                    "image": routine.image,
                    "create_at": routine.create_at,  # 추가된 필드
                    "url": f"https://www.likelion-start.site/api/celeb/{routine.celebrity.id}/"  # Celeb 페이지 URL
                })
            return routine_data

        new_update_data = create_routine_data(latest_routines)
        hot_routine_data = create_routine_data(hot_routines)
        user_routine_data = create_routine_data(user_routines)

        return Response({
            "theme": theme_data,
            "new_routine": new_update_data,
            "user_routine": user_routine_data,
            "hot_routine": hot_routine_data,
        })

            
