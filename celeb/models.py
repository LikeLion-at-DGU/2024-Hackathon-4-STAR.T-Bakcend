from django.db import models
from routine.models import Routine

class Celeb(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    photo = models.URLField(max_length=300)
    routines = models.ManyToManyField(Routine, related_name='celebrities', blank=True)

    def __str__(self):
        return self.name