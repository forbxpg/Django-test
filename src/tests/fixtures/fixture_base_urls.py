"""Модуль для фикстур базового Django приложения."""

from django.urls import reverse
import pytest


# BaseDjango URL fixtures
@pytest.fixture
def ads_list_url():
    return reverse("ads:ad-list")


@pytest.fixture
def ads_create_url():
    return reverse("ads:ad-create")


@pytest.fixture
def ads_detail_url(ad_one):
    return reverse("ads:ad-detail", kwargs={"pk": ad_one.pk})


@pytest.fixture
def ads_update_url(ad_one):
    return reverse("ads:ad-update", kwargs={"pk": ad_one.pk})


@pytest.fixture
def ads_delete_url(ad_one):
    return reverse("ads:ad-delete", kwargs={"pk": ad_one.pk})


@pytest.fixture
def exchange_proposal_list_url():
    return reverse("exchanges:exchanges-list")


@pytest.fixture
def exchange_proposal_create_url():
    return reverse("exchanges:create-exchange")


@pytest.fixture
def exchange_proposal_detail_url(exchange_proposal):
    return reverse(
        "exchanges:exchange-detail", kwargs={"pk": exchange_proposal.pk}
    )


@pytest.fixture
def exchange_proposal_create_via_ad_url(ad_one):
    return reverse("exchanges:create-exchange-ad", kwargs={"pk": ad_one.pk})
