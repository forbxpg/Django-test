"""Глобальный файл маршрутизации проекта."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("core.urls")),
    path("ads/", include("ads.urls")),
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

if settings.BROWSER_RELOAD:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
