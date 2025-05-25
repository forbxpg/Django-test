"""Модуль представлений для работы с моделью обменов."""

from django.db import models
from rest_framework import viewsets, permissions

from api.v1.serializers import (
    ExchangeStatusSerializer,
    ExchangeReadSerializer,
    ExchangeWriteSerializer,
)
from exchanges.models import ExchangeProposal


class ExchangeViewSet(viewsets.ModelViewSet):
    """Представление для работы с предложениями обмена."""

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.select_related(
            "ad_sender__user",
            "ad_receiver__user",
        ).filter(
            models.Q(ad_sender__user=user) | models.Q(ad_receiver__user=user)
        )

    def get_serializer_class(self):
        if self.action == "create":
            return ExchangeWriteSerializer
        return ExchangeReadSerializer
