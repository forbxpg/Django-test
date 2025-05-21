"""Модуль для базовых утилит проекта."""

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AdConditionChoices(TextChoices):
    """Класс для выбора состояния объявления."""

    NEW = "new", _("Новое")
    USED = "used", _("Б/У")


class ExchangeStatusChoices(TextChoices):
    """Класс для выбора статуса обмена."""

    PENDING = "pending", _("В ожидании")
    ACCEPTED = "accepted", _("Принято")
    REJECTED = "rejected", _("Отклонено")

