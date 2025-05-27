"""Модуль форм для работы с объявлениями."""

from django import forms
from django.utils.translation import gettext_lazy as _

from core import config
from .models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ("title", "description", "category", "image", "condition")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": config.DEFAULT_CSS_CLASS,
                    "placeholder": _("Введите название объявления"),
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": config.TEXT_INPUT_ROWS,
                    "class": config.DEFAULT_CSS_CLASS,
                    "placeholder": _("Введите описание объявления"),
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": config.DEFAULT_CSS_CLASS,
                    "placeholder": _("Выберите категорию"),
                }
            ),
            "condition": forms.Select(
                attrs={
                    "class": config.DEFAULT_CSS_CLASS,
                    "placeholder": _("Выберите состояние"),
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": config.DEFAULT_CSS_CLASS + " custom-file-input",
                    "placeholder": _("Выберите изображение"),
                }
            ),
        }
        labels = {"category": _("Категория"), "condition": _("Состояние")}
