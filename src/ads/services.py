"""Сервисы для работы с объявлениями."""

from django.db import models
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


def check_is_ad_related_to_sender_or_receiver(ad, current_user):
    """Проверяет, связано ли объявление с отправителем или получателем.
    Возвращает True, если объявление связано с отправителем или получателем,
    иначе возвращает False.
    """
    return ExchangeProposal.objects.filter(
        models.Q(ad_sender=ad, ad_sender__user=current_user)
        | models.Q(ad_receiver=ad, ad_receiver__user=current_user),
    ).exists()
