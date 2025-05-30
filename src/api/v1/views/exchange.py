"""Модуль представлений для работы с моделью обменов."""

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, response, status, filters
from rest_framework.decorators import action

from api.v1.filters import ExchangeFilterSet
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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ExchangeFilterSet
    search_fields = ("ad_sender__title", "ad_receiver__title")

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
        if proposal.status in (ExchangeStatusChoices.ACCEPTED,):
            return response.Response(
                {"detail": "Предложение уже было обменено"},
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        if proposal.status in (
            ExchangeStatusChoices.REJECTED,
            ExchangeStatusChoices.ACCEPTED,
        ):
            return response.Response(
                {"detail": "Предложение уже было обменено или отклонено."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        proposal.status = ExchangeStatusChoices.REJECTED
        proposal.save(update_fields=["status"])
        return response.Response(
            ExchangeReadSerializer(proposal).data,
            status=status.HTTP_200_OK,
        )
