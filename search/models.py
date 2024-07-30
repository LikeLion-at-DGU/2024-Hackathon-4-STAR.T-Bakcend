from django.db import models
from rest_framework import serializers

class Theme(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
    
