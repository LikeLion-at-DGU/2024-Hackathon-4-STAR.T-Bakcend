from django.contrib import admin
from .models import UserRoutine, PersonalSchedule, MonthlyTitle, UserRoutineCompletion

# Register your models here.

admin.site.register(UserRoutine)
admin.site.register(PersonalSchedule)
admin.site.register(MonthlyTitle)
admin.site.register(UserRoutineCompletion)