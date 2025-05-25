"""Модуль представлений для объявлений."""

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from ads.models import Ad
from ads.services import (
    get_not_exchanged_ads_queryset,
    check_is_ad_related_to_sender_or_receiver,
)
from api.v1.filters import AdFilterSet
from api.v1.pagination import PageNumberPagination
from api.v1.serializers import (
    AdSerializer,
    ExchangeWriteSerializer,
)
from api.v1.permissions import IsAdOwnerOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с объявлениями."""

    queryset = get_not_exchanged_ads_queryset()
    serializer_class = AdSerializer
    permission_classes = (IsAdOwnerOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = AdFilterSet
    search_fields = ("title", "description")

    def get_object(self):
        """Возвращает объект объявления, если объявление
        обменено и не связано с отправителем или получателем,
        то возвращает 404 Not Found.
        """
        ad = get_object_or_404(
            Ad.objects.select_related("user", "category"),
            pk=self.kwargs.get("pk"),
        )
        if ad.is_exchanged:
            if not check_is_ad_related_to_sender_or_receiver(
                ad, self.request.user
            ):
                return Response(
                    {
                        "detail": "Объявление не найдено или уже было обменено.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        return ad

    @action(
        methods=["post"],
        detail=True,
        url_path="propose",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def propose(self, request, *args, **kwargs):
        """Предложить обмен для объявления."""
        ad = self.get_object()
        serializer = ExchangeWriteSerializer(
            data={
                "ad_receiver": ad.id,
                "ad_sender": request.data.get("ad_sender"),
                "comment": request.data.get("comment", ""),
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
