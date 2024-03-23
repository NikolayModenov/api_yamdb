from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers


def validate_year(value):
    """Проверка значения в поле year, модели Title."""

    if value > timezone.now().year:
        raise ValidationError('Год должен быть меньше текущего года.')


def validate_username(username):
    if username == 'me':
        raise serializers.ValidationError('Неверное имя пользователя.')
