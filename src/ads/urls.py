"""Маршруты приложения ads."""

from django.urls import path

from . import views


app_name = "ads"

urlpatterns = [
    path("", views.ads_list_view, name="ads-list"),
    path("<int:ad_id>/", views.ad_detail_view, name="ad-detail"),
]


