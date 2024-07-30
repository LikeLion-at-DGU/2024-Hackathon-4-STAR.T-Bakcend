from rest_framework import viewsets
from rest_framework.response import Response
from .models import Celeb
from .serializers import CelebSerializer

class CelebViewSet(viewsets.ModelViewSet):
    queryset = Celeb.objects.all()
    serializer_class = CelebSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)