from django.db import models

class Celeb(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    photo = models.URLField(max_length=300, default='https://cdn.pixabay.com/photo/2020/08/22/12/36/yoga-5508336_1280.png')

    def __str__(self):
        return self.name
