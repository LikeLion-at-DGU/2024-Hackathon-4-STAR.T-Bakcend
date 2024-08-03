from django.db import models
from rest_framework import serializers

class Theme(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.URLField(max_length=500,max_length=500,null=True, blank=True,default='https://cdn.pixabay.com/photo/2020/08/22/12/36/yoga-5508336_1280.png')

    def __str__(self):
        return self.title
    
