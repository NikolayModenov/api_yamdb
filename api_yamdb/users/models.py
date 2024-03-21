from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class YamdbUser(AbstractUser):
    password = models.CharField(max_length=128, null=True, blank=True)
    bio = models.TextField('Биография', null=True, blank=True)
    role = models.CharField(default="user", choices=ROLES, max_length=9)
    confirmation_code = models.CharField(
        # 'код API на почту',
        max_length=200,
        null=True,
        blank=True
    )
