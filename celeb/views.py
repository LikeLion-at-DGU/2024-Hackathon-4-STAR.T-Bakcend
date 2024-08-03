from rest_framework import viewsets
from .models import Celeb
from .serializers import CelebSerializer
from rest_framework.permissions import IsAuthenticated
class CelebViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Celeb.objects.all()
    serializer_class = CelebSerializer
    permission_classes = [IsAuthenticated]
    