from django.db import models
from celeb.models import Celeb
from search.models import Theme


class RoutineCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Routine(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ManyToManyField(RoutineCategory)
    celebrity = models.ForeignKey(Celeb, on_delete=models.CASCADE)
    image = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


