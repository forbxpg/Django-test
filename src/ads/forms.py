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
            "title": forms.TextInput(attrs={ "class": config.TITLE_CLASS, "placeholder": _("Введите название объявления") }),
            "description": forms.Textarea(attrs={ "rows": config.DESCRIPTION_ROWS, "class": config.DESCRIPTION_CLASS, "placeholder": _("Введите описание объявления") }),
            "category": forms.Select(attrs={ "class": config.CATEGORY_CLASS }),
            "condition": forms.Select(attrs={ "class": config.CONDITION_CLASS }),
            "image": forms.ClearableFileInput(attrs={ "class": config.IMAGE_CLASS }),
        }
        labels = {
            "title": _("Title"),
            "description": _("Description"),
            "category": _("Category"),
            "image": _("Image"),
            "condition": _("Condition"),
        }
