"""Сериализатор для категорий."""

from rest_framework import serializers

from ads.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий объявлений."""

    class Meta:
        model = Category
        fields = ("id", "name", "slug")
