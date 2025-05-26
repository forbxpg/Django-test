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
        if not ad_sender or not ad_receiver:
            raise forms.ValidationError(
                _("Пожалуйста, выберите оба объявления для обмена.")
            )
        if ad_sender == ad_receiver:
            raise forms.ValidationError(
                _("Нельзя обмениваться одним и тем же объявлением.")
            )
        if (
            ExchangeProposal.objects.filter(
                ad_sender=ad_sender,
                ad_receiver=ad_receiver,
            ).exists()
            or ExchangeProposal.objects.filter(
                ad_sender=ad_receiver,
                ad_receiver=ad_sender,
            ).exists()
        ):
            raise forms.ValidationError(
                _("Предложение обмена уже существует для этих объявлений.")
            )
        if ad_sender.user == ad_receiver.user:
            raise forms.ValidationError(
                _("Нельзя обмениваться своими собственными объявлениями.")
            )
        if ad_sender.is_exchanged or ad_receiver.is_exchanged:
            raise forms.ValidationError(
                _("Нельзя обмениваться уже обмененными объявлениями.")
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

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        if self.instance.status == utils.ExchangeStatusChoices.ACCEPTED:
            raise forms.ValidationError(
                _("Нельзя изменить статус уже завершенного обмена.")
            )
        return cleaned_data
