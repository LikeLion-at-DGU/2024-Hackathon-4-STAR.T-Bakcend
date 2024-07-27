from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
from routine.models import RoutineCategory

class User(AbstractUser):
    social_login_type = models.CharField(max_length=20)
    subscription_status = models.BooleanField(default=False)
    subscription_expiry_date = models.DateField(null=True, blank=True)
    preferred_routine_categories = models.ManyToManyField(RoutineCategory, blank=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # 그룹 및 권한 필드에 related_name을 설정하여 역참조 충돌을 피합니다.
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # 기본 'user_set' 대신 'custom_user_set' 사용
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',  # 도움말 텍스트
        related_query_name='custom_user'  # 기본 'user' 대신 'custom_user' 사용
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # 기본 'user_set' 대신 'custom_user_permissions_set' 사용
        blank=True,
        help_text='Specific permissions for this user.',  # 도움말 텍스트
        related_query_name='custom_user_permission'  # 기본 'user' 대신 'custom_user_permission' 사용
    )

    def __str__(self):
        return self.username
