"""Модуль для управления правами доступа к ручкам API."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Дает доступ на изменение объекта только владельцу объявления."""

    def has_object_permission(self, request, view, obj):
        """Проверяет права доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.user == request.user
        )
