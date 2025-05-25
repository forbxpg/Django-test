"""Маршруты приложения ads."""

from django.urls import path

from . import views


app_name = "ads"

urlpatterns = [
    path("", views.ads_list_view, name="ads-list"),
    path("<int:ad_id>/", views.ad_detail_view, name="ad-detail"),
    path("create/", views.ad_create_view, name="ad-create"),
    path("<int:ad_id>/update/", views.ad_update_view, name="ad-update"),
    path("<int:ad_id>/delete/", views.ad_delete_view, name="ad-delete"),
    path("categories/", views.category_list_view, name="category-list"),
]
