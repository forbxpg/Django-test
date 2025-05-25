"""Представление категорий товаров."""

from rest_framework.viewsets import ReadOnlyModelViewSet

from ads.models import Category
from api.v1.serializers import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    """Представление категорий товаров."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "slug"
