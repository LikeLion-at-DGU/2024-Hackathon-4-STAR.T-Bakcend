from django.db import models


class RoutineCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Routine(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ManyToManyField(RoutineCategory)
    image = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    theme = models.ManyToManyField('search.Theme')  # use ManyToManyField
    popular =models.IntegerField(default=0)
    create_at = models.DateField(null = True)
    
    

    def __str__(self):
        return self.title

    def get_celebrity(self):
        from celeb.models import Celeb
        return Celeb.objects.filter(routines=self)

# # Use string reference for the ForeignKey field #admin 페이지에 접근이 안되서 필드를 추가했습니다.

Routine.add_to_class('celebrity', models.ForeignKey('celeb.Celeb', on_delete=models.CASCADE))
