from django.db import models
<<<<<<< HEAD

=======
>>>>>>> a616658c7ba8b5b7e99241f5b2ca36ec616f8260

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
    theme = models.ForeignKey('search.Theme', on_delete=models.CASCADE)  # use string reference

    def __str__(self):
        return self.title

    def get_celebrity(self):
        from celeb.models import Celeb
        return Celeb.objects.filter(routines=self)

# Use string reference for the ForeignKey field
Routine.add_to_class('celebrity', models.ForeignKey('celeb.Celeb', on_delete=models.CASCADE))
