from django.db import models
from user.models import User
from celeb.models import Celeb

class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    celebrity = models.ForeignKey(Celeb, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.celebrity.name} - {self.score}"
