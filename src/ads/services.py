"""Сервисы для работы с объявлениями."""

from django.shortcuts import get_object_or_404

from core.utils import AdConditionChoices, ExchangeStatusChoices
from exchanges.models import ExchangeProposal
from .models import Ad, Category


def get_ads_queryset():
    """Получает queryset для всех объявлений
    с user и category с применением JOIN.
    """
    return Ad.objects.select_related(
        "user",
        "category",
    )


def get_excluded_ad_ids():
    """Получает список ID объявлений, которые уже были обменены."""
    ids = ExchangeProposal.objects.filter(
        status=ExchangeStatusChoices.ACCEPTED
    ).values_list("ad_sender", "ad_receiver")
    return {ad_id for pair in ids for ad_id in pair if ad_id}
