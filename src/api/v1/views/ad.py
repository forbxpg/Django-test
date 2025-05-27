"""Модуль представлений для объявлений."""

from django.http.response import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
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

    serializer_class = AdSerializer
    permission_classes = (IsAdOwnerOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = AdFilterSet
    search_fields = ("title", "description")

    def get_queryset(self):
        if self.action == "list":
            return get_not_exchanged_ads_queryset()
        return Ad.objects.select_related(
            "category",
            "user",
        )

    def get_object(self):
        """Переопределение метода получения объекта
        для проверки прав доступа.
        """
        ad = super().get_object()
        if ad.is_exchanged:
            if not check_is_ad_related_to_sender_or_receiver(
                ad, self.request.user
            ):
                raise Http404(_("Объявление не найдено или уже обменено."))
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
