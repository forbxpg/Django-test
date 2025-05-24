"""Формы для обработки модели обменов объявлений."""

from django import forms
from django.utils.translation import gettext_lazy as _

from core import config, utils
from .models import ExchangeProposal


class ExchangeForm(forms.ModelForm):
    """Форма для создания обмена объявлениями."""

    class Meta:
        model = ExchangeProposal
        fields = (
            "ad_sender",
            "ad_receiver",
            "comment",
        )
        widgets = {
            "ad_sender": forms.Select(
                attrs={
                    "class": config.TITLE_CLASS,
                },
            ),
            "ad_receiver": forms.Select(
                attrs={
                    "class": config.TITLE_CLASS,
                },
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": config.TITLE_CLASS,
                    "rows": config.DESCRIPTION_ROWS,
                },
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        ad_sender = cleaned_data.get("ad_sender")
        ad_receiver = cleaned_data.get("ad_receiver")
        if ad_sender == ad_receiver:
            raise forms.ValidationError(
                _("Нельзя обмениваться одним и тем же объявлением.")
            )
        if ExchangeProposal.objects.filter(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
        ).exists():
            raise forms.ValidationError(
                _("Предложение обмена уже существует для этих объявлений.")
            )
        return cleaned_data


class ExchangeStatusForm(forms.ModelForm):
    """Форма для изменения статуса предложения обмена."""

    class Meta:
        model = ExchangeProposal
        fields = ("status",)
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": config.TITLE_CLASS,
                },
                choices=utils.ExchangeStatusChoices.choices,
            ),
        }
