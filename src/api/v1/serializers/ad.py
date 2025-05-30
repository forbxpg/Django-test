"""Сериализатор для модели объявлений."""

from rest_framework import serializers

from ads.models import Ad, Category


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для объявлений."""

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=True,
    )
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "description",
            "user",
            "image",
            "condition",
            "category",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
