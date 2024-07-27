from rest_framework import serializers
from .models import *

class RoutineSerializer(serializers.ModelSerializer):

    class Meta:
        models = Routine
        fields = '__all__'


class RoutineCategorySerializer(serializers.ModelSerializer):

    class Meta:
        models = RoutineCategory
        fields = [
            'name'
        ]