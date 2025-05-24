"""Модуль сигналов для обработки событий в приложении объявлений."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from exchanges.models import ExchangeProposal
from .models import Ad
from core.utils import ExchangeStatusChoices


@receiver(post_save, sender=ExchangeProposal)
def update_ad_status(sender, instance, created, **kwargs):
    """Обновляет статус объявления при создании
    или изменении предложения обмена.
    """
    if instance.status == ExchangeStatusChoices.ACCEPTED:
        ad_sender = instance.ad_sender
        ad_receiver = instance.ad_receiver
        for ad in (ad_sender, ad_receiver):
            if not ad.is_exchanged:
                ad.is_exchanged = True
                ad.save(update_fields=["is_exchanged"])
