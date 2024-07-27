from django.db import models
from user.models import User
from routine.models import Routine

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.title}"

class CalendarRoutine(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.calendar.user.username} - {self.routine.title} - {self.status}"
