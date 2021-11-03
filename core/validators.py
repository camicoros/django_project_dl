import datetime
from django.core.exceptions import ValidationError


def validate_date_edit(value):
    """
    Проверка, что дата редактирования не позже текущей даты
    """
    if value.date() > datetime.datetime.now().date():
        raise ValidationError('date can\'t be so late')