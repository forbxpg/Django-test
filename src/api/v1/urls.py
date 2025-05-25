"""Маршруты API v1."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views import CategoryViewSet, AdViewSet


v1_router = DefaultRouter()

v1_router.register("ads", AdViewSet, basename="ads")
v1_router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(v1_router.urls)),
]
