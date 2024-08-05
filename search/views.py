from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Theme
from celeb.models import Celeb
from routine.models import Routine
from .serializers import ThemeSerializer, CelebritySerializer, RoutineSerializer

class SearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] # 로그인 토큰 받고 다시 활성화
    def list(self, request):
        data = request.query_params.get('data', None)
        if not data:
            return Response({"detail": "Search term not provided."}, status=400)

        # 검색어를 이용해 연예인, 루틴, 테마를 검색
        celebrities = Celeb.objects.filter(name__icontains=data) | Celeb.objects.filter(profession__icontains=data)
        routines = Routine.objects.filter(title__icontains=data) #| Routine.objects.filter(content__icontains=data)
        themes = Theme.objects.filter(title__icontains=data) #| Theme.objects.filter(content__icontains=data)
        ##
        theme_routines = Routine.objects.all()
        # 직렬화
        #celeb_serializer = CelebritySerializer(celebrities, many=True)
        # routine_serializer = RoutineSerializer(routines, many=True)
        #theme_serializer = ThemeSerializer(themes, many=True)

        routine_data = []
        for routine in routines:
            # routine.celebrity가 유효한 Celebrity 객체인지 확인
            if not hasattr(routine.celebrity, 'id'):
                continue  # celebrity가 유효하지 않으면 무시
            routine_data.append({
                "id": routine.id,
                "title": routine.title,
                "profession": [routine.celebrity.name],
                "image": routine.image,
                "url": routine.celebrity.id  # Celeb 페이지 URL
            })       


        # 테마에 루틴 추가
        theme_data = []
        for theme in themes:
            routines_in_theme = theme_routines.filter(theme=theme)
            routines_serializer = RoutineSerializer(routines_in_theme, many=True)
            theme_data.append({
                "id": theme.id,
                "title": theme.title,
                "profession": [routine['title'] for routine in routines_serializer.data],
                "image": theme.image,  # 테마 페이지 대표 사진 URL 사용
                "url": theme.id # 실제 테마 페이지 URL을 여기에 추가합니다.
            })


        celeb_data = []
        for celeb in celebrities:
            celeb_data.append({
                "id": celeb.id,
                "title": celeb.name,
                "profession": [celeb.profession],
                "image": celeb.photo,
                "url": celeb.id ,    # 테마 페이지 대표 사진 URL 사용
            })
    
        return Response({
            "인물": celeb_data,
            "루틴": routine_data,
            "테마": theme_data,
        })
    

class ThemeDetailViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        try:
            theme = Theme.objects.get(pk=pk)
        except Theme.DoesNotExist:
            return Response({"detail": "Theme not found."}, status=404)
        
        theme_serializer = ThemeSerializer(theme)
        routines = Routine.objects.filter(theme=theme)
        routine_serializer = RoutineSerializer(routines, many=True)
        return Response({
            "theme_id": theme.id,
            "theme_title": theme.title,
            "theme_content": theme.content,
            "theme_image" : theme.image,
            "routine": routine_serializer.data
        })
