"""Модель сериализатора пользователя."""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from core.config import PHONE_REGION


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    phone = PhoneNumberField(
        required=False,
        allow_blank=True,
        allow_null=True,
        region=PHONE_REGION,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
        )
