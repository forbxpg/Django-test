"""Маршруты для API."""

from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


app_name = "api"


schema_view = get_schema_view(
    openapi.Info(
        title="ShareVito API",
        default_version="v1",
        description="Документация к API приложения ShareVito",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="dwizard80@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("v1/", include("api.v1.urls")),
    path(
        "docs/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
