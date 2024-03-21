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
        unique=True,
    )
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(default="Пользователь", choices=ROLES, max_length=9)
    confirmation_code = models.CharField(
        # 'код API на почту',
        max_length=200,
        null=True,
        blank=True
    )
    REQUIRED_FIELDS = ['email', 'confirmation_code']
    password = models.CharField(max_length=128, blank=True, null=True)
