from django.db import models
from routine.models import Routine

class Celeb(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    photo = models.URLField(max_length=500, default='https://cdn.pixabay.com/photo/2020/08/22/12/36/yoga-5508336_1280.png')
    routines = models.ManyToManyField(Routine, related_name='celebrities', blank=True)


    def __str__(self):
        return self.name