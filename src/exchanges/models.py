"""Модели приложения обмена."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from ads.models import Ad
from core import config
from core.utils import ExchangeStatusChoices


class ExchangeProposal(models.Model):
    """Модель для предложений обмена."""

    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="exchange_proposals_sent",
        verbose_name=_("Объявление отправителя"),
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="exchange_proposals_received",
        verbose_name=_("Объявление получателя"),
    )
    comment = models.TextField(
        _("Комментарий к предложению"),
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=config.EXCHANGE_STATUS_LENGTH,
        choices=ExchangeStatusChoices.choices,
        default=ExchangeStatusChoices.PENDING,
        verbose_name=_("Статус предложения обмена"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата предложения обмена"),
    )

    class Meta:
        verbose_name = _("Предложение обмена")
        verbose_name_plural = _("Предложения обмена")
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["ad_sender", "ad_receiver"],
                name="unique_exchange_proposal",
                violation_error_message=_(
                    "Предложение обмена уже существует для этих объявлений."
                ),
            ),
            models.CheckConstraint(
                check=~models.Q(ad_sender=models.F("ad_receiver")),
                name="ad_sender_not_equal_ad_receiver",
                violation_error_message=_(
                    "Объявления отправителя и получателя не могут быть одинаковыми."
                ),
            ),
        ]
        indexes = [
            models.Index(fields=["ad_sender"], name="ad_sender_idx"),
            models.Index(fields=["ad_receiver"], name="ad_receiver_idx"),
        ]

    def __str__(self):
        return _("Предложение обмена товара %(ad_sender)s на товар %(ad_receiver)s") % {
            "ad_sender": self.ad_sender.title,
            "ad_receiver": self.ad_receiver.title,
        }
