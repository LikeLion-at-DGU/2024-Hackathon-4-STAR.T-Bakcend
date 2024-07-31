from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Theme
from celeb.models import Celeb
from routine.models import Routine
from .serializers import ThemeSerializer, CelebritySerializer, RoutineSerializer

class SearchViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated] # 로그인 토큰 받고 다시 활성화
    def list(self, request):
        data = request.query_params.get('data', None)
        if not data:
            return Response({"detail": "Search term not provided."}, status=400)

        # 검색어를 이용해 연예인, 루틴, 테마를 검색
        celebrities = Celeb.objects.filter(name__icontains=data) | Celeb.objects.filter(profession__icontains=data)
        routines = Routine.objects.filter(title__icontains=data) #| Routine.objects.filter(content__icontains=data)
        themes = Theme.objects.filter(title__icontains=data) #| Theme.objects.filter(content__icontains=data)
        print(celebrities)
        print(themes)
        # 직렬화
        celeb_serializer = CelebritySerializer(celebrities, many=True)
        routine_serializer = RoutineSerializer(routines, many=True)
        theme_serializer = ThemeSerializer(themes, many=True)

        # 테마에 루틴 추가
        theme_data = []
        for theme in themes:
            routines_in_theme = routines.filter(theme=theme)
            routines_serializer = RoutineSerializer(routines_in_theme, many=True)
            theme_data.append({
                "id": theme.id,
                "title": theme.title,
                "routine_title": [routine['title'] for routine in routines_serializer.data],
                "image": theme.image,  # 테마 페이지 대표 사진 URL 사용
                "url": f"http://52.78.17.82/api/theme/{theme.id}/"  # 실제 테마 페이지 URL을 여기에 추가합니다.
            })
    
        return Response({
            "celeb": celeb_serializer.data,
            #"routines": routine_serializer.data,
            "theme": theme_data,
        })
    

class ThemeDetailViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]

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
