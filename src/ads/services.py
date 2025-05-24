"""Сервисы для работы с объявлениями."""

from django.shortcuts import get_object_or_404

from core.utils import AdConditionChoices, ExchangeStatusChoices
from exchanges.models import ExchangeProposal
from .models import Ad, Category


def get_not_exchanged_ads_queryset():
    """Получает queryset для всех объявлений
    с user и category с применением JOIN-запроса.

    Исключает объявления, которые уже были обменены.
    """
    return Ad.objects.select_related(
        "user",
        "category",
    ).filter(
        is_exchanged=False,
    )
