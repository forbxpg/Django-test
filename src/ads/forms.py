from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core import config
from .models import Ad, Category


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ("title", "description", "category", "image", "condition")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": config.TITLE_CLASS,
                    "placeholder": _("Введите название объявления"),
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": config.DESCRIPTION_ROWS,
                    "class": config.DESCRIPTION_CLASS,
                    "placeholder": _("Введите описание объявления"),
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": config.CATEGORY_CLASS,
                    "placeholder": _("Выберите категорию"),
                }
            ),
            "condition": forms.Select(
                attrs={
                    "class": config.CONDITION_CLASS,
                    "placeholder": _("Выберите состояние"),
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": config.IMAGE_CLASS + " custom-file-input",
                    "placeholder": _("Выберите изображение"),
                }
            ),
        }
        labels = {"category": _("Категория"), "condition": _("Состояние")}

