from django.db import models

class Celeb(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    photo = models.URLField(max_length=200)

    def __str__(self):
        return self.name

    def get_routines(self):
        from routine.models import Routine
        return self.routines.all()

# Use string reference for the ManyToManyField
Celeb.add_to_class('routines', models.ManyToManyField('routine.Routine'))
