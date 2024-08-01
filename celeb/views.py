from rest_framework import viewsets
from .models import Celeb
from .serializers import CelebSerializer

class CelebViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Celeb.objects.all()
    serializer_class = CelebSerializer