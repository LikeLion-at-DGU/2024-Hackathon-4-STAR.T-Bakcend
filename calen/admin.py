from django.contrib import admin
from .models import UserRoutine, UserRoutineCompletion, PersonalSchedule, MonthlyTitle

class UserRoutineAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__username', 'routine__title']
    list_display = ['user', 'routine', 'start_date', 'end_date']

admin.site.register(UserRoutine, UserRoutineAdmin)

class UserRoutineCompletionAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'routine__routine__title']
    list_display = ['user', 'routine', 'date', 'completed']

admin.site.register(UserRoutineCompletion, UserRoutineCompletionAdmin)

class PersonalScheduleAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'title', 'description']
    list_display = ['user', 'title', 'description', 'date', 'completed']

admin.site.register(PersonalSchedule, PersonalScheduleAdmin)

class MonthlyTitleAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'month', 'title']
    list_display = ['user', 'month', 'title']

admin.site.register(MonthlyTitle, MonthlyTitleAdmin)
