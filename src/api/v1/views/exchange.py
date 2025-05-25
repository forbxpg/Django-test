"""Модуль представлений для работы с моделью обменов."""

from django.db import models
from rest_framework import viewsets, response, status
from rest_framework.decorators import action

from api.v1.pagination import PageNumberPagination
from api.v1.serializers import (
    ExchangeReadSerializer,
    ExchangeWriteSerializer,
)
from api.v1.permissions import IsExchangeParticipant, IsExchangeReceiver
from core.utils import ExchangeStatusChoices
from exchanges.models import ExchangeProposal


class ExchangeViewSet(viewsets.ModelViewSet):
    """Представление для работы с предложениями обмена."""

    permission_classes = (IsExchangeParticipant,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.select_related(
            "ad_sender__user",
            "ad_receiver__user",
        ).filter(
            models.Q(ad_sender__user=user) | models.Q(ad_receiver__user=user)
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ExchangeWriteSerializer
        return ExchangeReadSerializer

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(IsExchangeReceiver,),
        url_path="accept",
    )
    def accept_proposal(self, request, *args, **kwargs):
        """Принять предложение обмена."""
        proposal = self.get_object()
        proposal.status = ExchangeStatusChoices.ACCEPTED
        proposal.save(update_fields=["status"])
        return response.Response(
            ExchangeReadSerializer(proposal).data,
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(IsExchangeReceiver,),
        url_path="reject",
    )
    def reject_proposal(self, request, *args, **kwargs):
        """Отклонить предложение обмена."""
        proposal = self.get_object()
        proposal.status = ExchangeStatusChoices.REJECTED
        proposal.save(update_fields=["status"])
        return response.Response(
            ExchangeReadSerializer(proposal).data,
            status=status.HTTP_200_OK,
        )
