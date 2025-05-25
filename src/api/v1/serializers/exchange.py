"""Сериализаторы для модели обменов."""

from rest_framework import serializers

from ads.services import get_not_exchanged_ads_queryset
from core.utils import ExchangeStatusChoices
from exchanges.models import ExchangeProposal


class ExchangeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения предложений обмена."""

    class Meta:
        model = ExchangeProposal
        fields = (
            "id",
            "ad_sender",
            "ad_receiver",
            "comment",
            "status",
            "created_at",
        )


class ExchangeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи предложений обмена."""

    ad_sender = serializers.PrimaryKeyRelatedField(
        queryset=get_not_exchanged_ads_queryset(),
        write_only=True,
    )
    ad_receiver = serializers.PrimaryKeyRelatedField(
        queryset=get_not_exchanged_ads_queryset(),
        write_only=True,
    )

    class Meta:
        model = ExchangeProposal
        fields = (
            "ad_sender",
            "ad_receiver",
            "comment",
        )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ExchangeProposal.objects.all(),
                fields=("ad_sender", "ad_receiver"),
                message="Предложение обмена уже существует.",
            )
        ]

    def validate(self, attrs):
        """Проверка на возможность обмена."""
        ad_sender = attrs.get("ad_sender")
        ad_receiver = attrs.get("ad_receiver")
        if ad_sender == ad_receiver:
            raise serializers.ValidationError(
                "Нельзя обменивать объявление на само себя."
            )
        if ad_sender.is_exchanged or ad_receiver.is_exchanged:
            raise serializers.ValidationError(
                "Нельзя обмениваться уже обмененными объявлениями."
            )
        if (
            ExchangeProposal.objects.filter(
                ad_sender=ad_sender,
                ad_receiver=ad_receiver,
            ).exists()
            or ExchangeProposal.objects.filter(
                ad_sender=ad_receiver,
                ad_receiver=ad_sender,
            ).exists()
        ):
            raise serializers.ValidationError(
                "Предложение обмена уже существует для этих объявлений."
            )
        if ad_sender.user == ad_receiver.user:
            raise serializers.ValidationError(
                "Нельзя обменивать свои собственные объявления."
            )
        return attrs

    def to_representation(self, instance):
        """Преобразование данных для ответа."""
        return ExchangeReadSerializer(instance).data
