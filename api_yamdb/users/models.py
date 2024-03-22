from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class YamdbUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты.', max_length=254, unique=True,
    )
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(default="user", choices=ROLES, max_length=9)
    confirmation_code = models.CharField(
        'Код подтверждения', max_length=200, null=True, blank=True
    )
    REQUIRED_FIELDS = ['email', 'confirmation_code']
    password = models.CharField(
        'Пароль.', max_length=128, blank=True, null=True
    )
