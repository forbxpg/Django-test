from django.urls import path

from . import views


app_name = "exchanges"

urlpatterns = [
    path(
        "",
        views.exchange_list_view,
        name="exchanges-list",
    ),
    path(
        "create/",
        views.exchange_create_view,
        name="create-exchange",
    ),
    path(
        "create/<int:ad_id>/",
        views.exchange_create_view,
        name="create-exchange-ad",
    ),
    path(
        "<int:proposal_id>/",
        views.exchange_detail_view,
        name="exchange-detail",
    ),
]
