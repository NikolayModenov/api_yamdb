from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class YamdbUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(default="user", choices=ROLES, max_length=9)
