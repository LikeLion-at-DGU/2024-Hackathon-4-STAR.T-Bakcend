from django.db import models
from accounts.models import User
from celeb.models import Celeb
from django.db.models import UniqueConstraint

class CelebScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    celeb = models.ForeignKey(Celeb, on_delete=models.CASCADE)
    score = models.IntegerField()

    # 동일한 사용자가 동일한 셀럽에 대해 여러개의 점수를 가질 수 없음
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'celeb'], name='unique_user_celeb')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.celeb.name} - {self.score}"
