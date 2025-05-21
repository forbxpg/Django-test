"""Фильтры для объявлений."""

import django_filters
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Ad, Category
from core.utils import AdConditionChoices


class AdFilter(django_filters.FilterSet):
    """Фильтрация объявлений."""

    category = django_filters.ModelChoiceFilter(
        field_name="category",
        queryset=Category.objects.all(),
        to_field_name="slug",
        label=_("Категория"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    condition = django_filters.ChoiceFilter(
        field_name="condition",
        choices=AdConditionChoices.choices,
        label=_("Статус объявления"),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Ad
        fields = {
            "title": ["icontains"],
            "description": ["icontains"],
            "user": ["exact"],
        }
