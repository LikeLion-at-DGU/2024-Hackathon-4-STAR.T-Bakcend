from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CelebScore
from .serializers import CelebScoreSerializer
from django.shortcuts import get_object_or_404
from celeb.models import Celeb

class CelebScoreViewSet(viewsets.ModelViewSet):
    queryset = CelebScore.objects.all()
    serializer_class = CelebScoreSerializer

    def get_queryset(self):
        user = self.request.user
        return CelebScore.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def celeb_scores(self, request):
        user = request.user
        scores = CelebScore.objects.filter(user=user)
        serializer = CelebScoreSerializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_score(self, request, pk=None):
        user = request.user
        celeb = get_object_or_404(Celeb, pk=pk)
        score = request.data.get('score')

        celeb_score, created = CelebScore.objects.update_or_create(
            user=user,
            celeb=celeb,
            defaults={'score': score}
        )

        serializer = CelebScoreSerializer(celeb_score)
        return Response(serializer.data)