"""Сериализаторы для модели обменов."""

from rest_framework import serializers

from exchanges.models import ExchangeProposal



class ExchangeSerializer(serializers.ModelSerializer):
    """Сериализатор для предложений обмена."""

    class Meta:
        model = ExchangeProposal
        fields = (
            "id",
            "ad_sender",
            "ad_receiver",

        )