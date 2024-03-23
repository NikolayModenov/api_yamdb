from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка значения в поле year, модели Title."""

    if value > timezone.now().year:
        raise ValidationError('Год не должен быть больше текущего года.')
