"""Модуль представлений для объявлений."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, response

from ads.models import Ad
from ads.services import (
    get_not_exchanged_ads_queryset,
    check_is_ad_related_to_sender_or_receiver,
)
from api.v1.serializers import AdSerializer
from api.v1.permissions import IsOwnerOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с объявлениями."""

    queryset = get_not_exchanged_ads_queryset()
    serializer_class = AdSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self):
        """Возвращает объект объявления, если объявление
        обменено и не связано с отправителем или получателем,
        то возвращает 404 Not Found.
        """
        ad = get_object_or_404(
            Ad.objects.select_related("user", "receiver"),
            pk=self.kwargs.get("pk"),
        )
        if not check_is_ad_related_to_sender_or_receiver(
            ad, self.request.user
        ):
            return response.Response(
                {"detail": "Объявление не найдено или уже было обменено."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return ad
