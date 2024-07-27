from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from routine.models import RoutineCategory
class User(AbstractUser):
    social_login_type = models.CharField(max_length=20)
    subscription_status = models.BooleanField(default=False)
    subscription_expiry_date = models.DateField(null=True, blank=True)
    preferred_routine_categories = models.ManyToManyField(RoutineCategory, blank=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.username
