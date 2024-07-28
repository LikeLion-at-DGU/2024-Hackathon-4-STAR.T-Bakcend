from rest_framework import viewsets,mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RoutineSerializer,RoutineCategorySerializer
from .models import Routine , RoutineCategory
from rest_framework.decorators import action

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    #permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail = False)
    def recommend(self, request):
        ran_routine = self.get_queryset().order_by("?").first()
        ran_routine_serializer =RoutineSerializer(ran_routine)
        return Response(ran_routine_serializer.data)
    