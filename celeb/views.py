from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Celeb
from .serializers import CelebSerializer

class CelebViewSet(viewsets.ModelViewSet):
    queryset = Celeb.objects.all()
    serializer_class = CelebSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context