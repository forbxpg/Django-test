"""Фильтры для API v1."""

import django_filters
from django.db import models
from ads.models import Ad
from exchanges.models import ExchangeProposal
from core.utils import AdConditionChoices, ExchangeStatusChoices


class AdFilterSet(django_filters.FilterSet):
    """Фильтры для объявлений."""

    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr="iexact",
    )
    condition = django_filters.ChoiceFilter(
        field_name="condition",
        choices=AdConditionChoices.choices,
        lookup_expr="iexact",
    )

    class Meta:
        model = Ad
        fields = ("category", "condition")


class ExchangeFilterSet(django_filters.FilterSet):
    """Фильтры для предложений обмена."""

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=ExchangeStatusChoices.choices,
        lookup_expr="iexact",
    )
    ad_sender = django_filters.NumberFilter(
        field_name="ad_sender__id",
        lookup_expr="exact",
    )
    ad_receiver = django_filters.NumberFilter(
        field_name="ad_receiver__id",
        lookup_expr="exact",
    )

    class Meta:
        model = ExchangeProposal
        fields = ("status", "ad_sender", "ad_receiver")
