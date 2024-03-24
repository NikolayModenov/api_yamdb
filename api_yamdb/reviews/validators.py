import re

from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

from api_yamdb.settings import URL_PATH_NAME


def validate_year(value):
    """Проверка значения в поле year, модели Title."""

    if value > timezone.now().year:
        raise ValidationError(
            f'Год произведения - {value}, '
            f'не должен быть больше текущего года - {timezone.now().year}.'
        )
    return value


def validate_username(username):
    if username == URL_PATH_NAME:
        raise serializers.ValidationError(
            f'Неверное имя пользователя: {username}.'
        )
    if not re.fullmatch(r'^[\w.@+-]+\Z', username):
        raise ValidationError(
            'Введите действительное имя пользователя. '
            'username может содержать только латинские буквы, '
            'символы @/./+/-/_ и цифры.'
        )
    return username
