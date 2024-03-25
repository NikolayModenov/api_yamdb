import re

from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.serializers import ValidationError

from api_yamdb.settings import USER_URL_PATH_NAME


def validate_year(value):
    """Проверка значения в поле year, модели Title."""

    if value > timezone.now().year:
        raise ValidationError(
            f'Год произведения - {value}, '
            f'не должен быть больше текущего года - {timezone.now().year}.'
        )
    return value


def validate_username(username):
    if username == USER_URL_PATH_NAME:
        raise ValidationError(
            f'Неверное имя пользователя: {username}.'
        )
    check_symbols = re.sub(r'[\w.@+-]', '', username)
    if check_symbols:
        bad_symbols = "".join(set(check_symbols))
        raise ValidationError(
            'В Имени пользователя использованы запрещённые символы: '
            f'{bad_symbols} '
            'Введите корректное имя пользователя. '
            'username может содержать только латинские буквы, '
            'символы @/./+/-/_ и цифры.'
        )
    return username
