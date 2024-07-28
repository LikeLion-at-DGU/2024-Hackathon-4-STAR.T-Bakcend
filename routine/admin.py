from django.contrib import admin
from .models import Routine,RoutineCategory

# Register your models here.

admin.site.register(Routine)
admin.site.register(RoutineCategory)