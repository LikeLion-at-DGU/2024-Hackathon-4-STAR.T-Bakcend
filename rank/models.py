from django.db import models
from accounts.models import User
from celeb.models import Celeb

class Rank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    celeb = models.ForeignKey(Celeb, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.celeb.name} - {self.score}"
