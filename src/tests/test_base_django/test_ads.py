from http import HTTPStatus

import pytest

from django.urls import reverse
from ads.models import Ad, Category
from exchanges.models import ExchangeProposal


@pytest.mark.django_db(transaction=True)
class TestBaseDjangoAds:

    ADS_LIST = reverse("ads:ads-list")
    AD_CREATE = reverse("ads:ad-create")

    def test_ads_list_no_auth(self, client, ad_one):
        response = client.get(self.ADS_LIST)
        assert response.status_code == HTTPStatus.OK
        assert response.context["page_obj"].object_list == [ad_one]
        assert "filter" in response.context

    def test_ads_list_with_auth(self, user_one_client, ad_one):
        response = user_one_client.get(self.ADS_LIST)
        assert response.status_code == HTTPStatus.OK
        assert response.context["page_obj"].object_list == [ad_one]
        assert "filter" in response.context

    def test_create_ad_no_auth(self, client, category_one):
        response = client.post(
            self.AD_CREATE,
            data={
                "title": "New Ad",
                "description": "Description for new ad",
                "category": category_one.id,
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        assert "/users/login/?next=/ads/" in response.url

    def test_create_ad_auth(self, user_one_client, category_one):
        response = user_one_client.post(
            self.AD_CREATE,
            data={
                "title": "New Ad",
                "description": "Description for new ad",
                "category": category_one.id,
                "condition": "new",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        ads = Ad.objects.all()
        assert len(ads) == 1
        ad = Ad.objects.first()
        assert response.url == reverse(
            "ads:ad-detail",
            kwargs={"ad_id": ad.id},
        )

    def test_update_ad(self, user_one_client, ad_one, category_two):
        response = user_one_client.post(
            reverse("ads:ad-update", kwargs={"ad_id": ad_one.id}),
            data={
                "title": "Updated Ad",
                "description": "Updated description",
                "category": category_two.id,
                "condition": "used",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        ad_one.refresh_from_db()
        assert ad_one.title == "Updated Ad"
        assert ad_one.description == "Updated description"
        assert ad_one.category == category_two
        assert response.url == reverse(
            "ads:ad-detail",
            kwargs={"ad_id": ad_one.id},
        )

    def test_update_ad_not_author(self, user_two_client, ad_one, category_two):
        response = user_two_client.post(
            reverse("ads:ad-update", kwargs={"ad_id": ad_one.id}),
            data={
                "title": "Updated Ad",
                "description": "Updated description",
                "category": category_two.id,
                "condition": "used",
            },
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        ad_one.refresh_from_db()
        assert ad_one.title != "Updated Ad"
        assert ad_one.description != "Updated description"
        assert ad_one.category != category_two

    def test_delete_ad(self, user_one_client, ad_one, category_two):
        response = user_one_client.post(
            reverse("ads:ad-delete", kwargs={"ad_id": ad_one.id}),
        )
        assert response.status_code == HTTPStatus.FOUND
        assert not Ad.objects.filter(id=ad_one.id).exists()
        assert response.url == reverse("ads:ads-list")

    def test_delete_ad_not_author(self, user_two_client, ad_one, category_two):
        response = user_two_client.post(
            reverse("ads:ad-delete", kwargs={"ad_id": ad_one.id}),
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert Ad.objects.filter(id=ad_one.id).exists()
