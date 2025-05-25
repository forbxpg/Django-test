"""Модуль для управления правами доступа к ручкам API."""

from rest_framework import permissions


class IsAdOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Дает доступ на изменение объекта только владельцу объявления."""

    def has_object_permission(self, request, view, obj):
        """Проверяет права доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.user == request.user
        )


class IsExchangeParticipant(permissions.BasePermission):
    """Проверяет, что пользователь является владельцем обмена."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.ad_sender.user
            or request.user == obj.ad_receiver.user
        )


class IsExchangeReceiver(permissions.BasePermission):
    """Проверяет, что пользователь является получателем обмена."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.ad_receiver.user
