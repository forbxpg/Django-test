"""Глобальный файл маршрутизации проекта."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("ads/", include("ads.urls")),
    path("", include("core.urls")),
    path("users/", include("users.urls")),
    path("exchanges/", include("exchanges.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
