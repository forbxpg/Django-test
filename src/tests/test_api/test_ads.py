from http import HTTPStatus

import pytest

from ads.models import Ad


@pytest.mark.django_db(transaction=True)
class TestAdsAPI:

    ADS_URL = "/api/v1/ads/"
    AD_DETAIL_URL = "/api/v1/ads/{pk}/"

    def test_ads_endpoint_no_auth(self, client):
        response = client.get(self.ADS_URL)
        assert response.status_code == HTTPStatus.OK
        assert "results" in response.data
        assert isinstance(response.data["results"], list)

    def test_create_ad_no_auth(self, client):
        response = client.post(
            self.ADS_URL,
            data={
                "title": "Test Ad",
                "description": "This is a test ad.",
                "category": "test",
            },
            format="json",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_ad_with_auth(
        self,
        api_user_one_client,
        api_user_one,
        api_category,
    ):
        data = {
            "title": "Test Ad",
            "description": "This is a test ad.",
            "category": api_category.slug,
        }
        response = api_user_one_client.post(self.ADS_URL, data=data)
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert Ad.objects.count() == 1

    def test_ad_update_not_author(self, client, api_ad_one, api_category_two):
        response = client.patch(
            self.AD_DETAIL_URL.format(pk=api_ad_one.pk),
            data={
                "description": "This ad has been updated.",
            },
            format="json",
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_ad_update_auth(
        self, api_user_one_client, api_ad_one, api_user_one, api_category_two
    ):
        data = {
            "title": "Updated Ad",
        }
        response = api_user_one_client.patch(
            self.AD_DETAIL_URL.format(pk=api_ad_one.pk),
            data=data,
            format="json",
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data["title"] == data["title"]
        assert response.data["description"] == api_ad_one.description
        assert response.data["title"] == Ad.objects.get(pk=api_ad_one.pk).title

    def test_ad_delete_not_author(self, api_user_two_client, api_ad_one):
        response = api_user_two_client.delete(
            self.AD_DETAIL_URL.format(pk=api_ad_one.pk),
            format="json",
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert Ad.objects.count() == 1

    def test_ad_delete_author(self, api_user_one_client, api_ad_one):
        response = api_user_one_client.delete(
            self.AD_DETAIL_URL.format(pk=api_ad_one.pk),
            format="json",
        )
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert Ad.objects.count() == 0

    def test_exchanged_ad_detail_no_participant(
        self,
        api_accepted_exchange,
        api_user_three_client,
        api_ad_one,
    ):
        response = api_user_three_client.get(
            self.AD_DETAIL_URL.format(pk=api_ad_one.pk)
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
