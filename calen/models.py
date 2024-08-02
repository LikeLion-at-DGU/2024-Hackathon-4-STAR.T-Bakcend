from django.conf import settings
from django.db import models
from routine.models import Routine
from project import settings

class UserRoutine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #AUTH_USER_MODEL에 대한 외래키
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if self.pk is None:  # 인스턴스가 새로 생성되는 경우
            self.routine.popular += 1
            self.routine.save()
        super().save(*args, **kwargs)


class UserRoutineCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    routine = models.ForeignKey(UserRoutine, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('routine', 'date') # 루틴과 조합 유일 -> 동일한 루틴에 대해 같은 날짜에 여러번 가능

class PersonalSchedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)

class MonthlyTitle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()
    title = models.CharField(max_length=200)