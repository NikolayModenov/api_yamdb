from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class YamdbUser(AbstractUser):
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        max_length=254,
        null=False,
        unique=True,
        blank=False,
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(default="user", choices=ROLES, max_length=9)
    confirmation_code = models.CharField(
        # 'код API на почту',
        max_length=200,
        null=True,
        blank=True
    )
