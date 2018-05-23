import datetime
from django.conf import settings
from django.utils import timezone


def to_datetime(date: datetime.date) -> datetime.datetime:
    value = datetime.datetime.combine(date, datetime.time.min)
    if settings.USE_TZ:
        return timezone.make_aware(value, timezone.get_current_timezone())
    return value


def get_current_month(date: datetime.date) -> datetime.date:
    return date.replace(day=1)


def get_next_month(date: datetime.date) -> datetime.date:
    """It's possible to raise ValueError on Dec 9999"""
    if date.month == 12:
        return date.replace(year=date.year + 1, month=1, day=1)
    else:
        return date.replace(month=date.month + 1, day=1)
