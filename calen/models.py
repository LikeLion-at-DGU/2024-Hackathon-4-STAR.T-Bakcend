# calendar/models.py
from django.contrib.auth.models import User
from django.db import models
from routine.models import Routine

class UserRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField(default=False)

class PersonalSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)

class MonthlyTitle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    title = models.CharField(max_length=200)