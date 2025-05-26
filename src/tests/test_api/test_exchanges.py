from http import HTTPStatus

import pytest

from ads.models import Ad
from exchanges.models import ExchangeProposal
from core.utils import ExchangeStatusChoices


@pytest.mark.django_db(transaction=True)
class TestExchangesAPI:

    EXCHANGES_URL = "/api/v1/exchanges/"
    EXCHANGE_DETAIL_URL = "/api/v1/exchanges/{pk}"
    PROPOSE_URL = "/api/v1/ads/{ad_pk}/propose/"
    ACCEPT_URL = "/api/v1/exchanges/{pk}/accept/"
    REJECT_URL = "/api/v1/exchanges/{pk}/reject/"

    def test_exchange_list_no_auth(self, client):
        response = client.get(self.EXCHANGES_URL)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_exchange_list_auth(
        self,
        api_user_one_client,
    ):
        response = api_user_one_client.get(self.EXCHANGES_URL)
        assert response.status_code == HTTPStatus.OK
        assert "results" in response.data
        assert isinstance(response.data["results"], list)
        assert len(response.data["results"]) == 0

    def test_create_exchange_no_auth(self, client, api_ad_one, api_ad_two):
        response = client.post(
            self.EXCHANGES_URL,
            data={
                "ad_sender": api_ad_one.pk,
                "ad_receiver": api_ad_two.pk,
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_exchange_with_self_user_ads(
        self,
        api_user_one_client,
        api_ad_two,
        api_ad_one,
    ):
        response = api_user_one_client.post(
            self.EXCHANGES_URL,
            data={
                "ad_sender": api_ad_one.pk,
                "ad_receiver": api_ad_two.pk,
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_exchange_with_equal_ads(
        self,
        api_user_one_client,
        api_ad_one,
    ):
        response = api_user_one_client.post(
            self.EXCHANGES_URL,
            data={
                "ad_sender": api_ad_one.pk,
                "ad_receiver": api_ad_one.pk,
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_exchange_with_not_exists_ads(
        self,
        api_user_one_client,
    ):
        response = api_user_one_client.post(
            self.EXCHANGES_URL,
            data={
                "ad_sender": 9999,  # Non-existent ad
                "ad_receiver": 8888,  # Non-existent ad
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_exchange_with_valid_data(
        self,
        api_user_one_client,
        api_ad_one,
        api_ad_three,
    ):
        response = api_user_one_client.post(
            self.EXCHANGES_URL,
            data={
                "ad_sender": api_ad_one.pk,
                "ad_receiver": api_ad_three.pk,
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["ad_sender"] == api_ad_one.pk
        assert response.data["ad_receiver"] == api_ad_three.pk
        assert ExchangeProposal.objects.count() == 1
        exchange = ExchangeProposal.objects.first()
        assert exchange.status == ExchangeStatusChoices.PENDING

    def test_create_exchange_with_already_exchanged_ads(
        self,
        api_user_one_client,
        api_ad_one,
        api_ad_three,
    ):
        # Mark ads as exchanged
        api_ad_one.is_exchanged = True
        api_ad_one.save()
        api_ad_three.is_exchanged = True
        api_ad_three.save()

        response = api_user_one_client.post(
            self.EXCHANGES_URL,
            data={
                "ad_sender": api_ad_one.pk,
                "ad_receiver": api_ad_three.pk,
            },
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_create_propose_via_ad_id_no_auth(
        self,
        client,
        api_ad_one,
        api_ad_two,
    ):
        response = client.post(
            self.PROPOSE_URL.format(ad_pk=api_ad_one.pk),
            data={
                "ad_receiver": api_ad_two.pk,
                "comment": "Test comment",
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_create_propose_via_ad_id_with_auth(
        self,
        api_user_one_client,
        api_ad_one,
        api_ad_three,
    ):
        response = api_user_one_client.post(
            self.PROPOSE_URL.format(ad_pk=api_ad_one.pk),
            data={
                "ad_sender": api_ad_three.pk,
                "comment": "Test comment",
            },
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["ad_sender"] == api_ad_three.pk
        assert response.data["ad_receiver"] == api_ad_one.pk
        assert ExchangeProposal.objects.count() == 1
        exchange = ExchangeProposal.objects.first()
        assert exchange.status == ExchangeStatusChoices.PENDING

    def test_accept_exchange_no_auth(
        self,
        client,
        api_ad_one,
        api_ad_three,
    ):
        exchange = ExchangeProposal.objects.create(
            ad_sender=api_ad_three,
            ad_receiver=api_ad_one,
        )
        response = client.post(
            self.ACCEPT_URL.format(pk=exchange.pk),
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_accept_exchange_with_auth(
        self,
        api_user_one_client,
        api_ad_one,
        api_ad_three,
    ):
        exchange = ExchangeProposal.objects.create(
            ad_sender=api_ad_three,
            ad_receiver=api_ad_one,
        )
        response = api_user_one_client.post(
            self.ACCEPT_URL.format(pk=exchange.pk),
        )
        assert response.status_code == HTTPStatus.OK
        exchange.refresh_from_db()
        assert exchange.status == ExchangeStatusChoices.ACCEPTED

    def test_reject_exchange_no_auth(
        self,
        client,
        api_ad_one,
        api_ad_three,
    ):
        exchange = ExchangeProposal.objects.create(
            ad_sender=api_ad_three,
            ad_receiver=api_ad_one,
        )
        response = client.post(
            self.REJECT_URL.format(pk=exchange.pk),
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_reject_exchange_with_auth(
        self,
        api_user_one_client,
        api_ad_one,
        api_ad_three,
    ):
        exchange = ExchangeProposal.objects.create(
            ad_sender=api_ad_three,
            ad_receiver=api_ad_one,
        )
        response = api_user_one_client.post(
            self.REJECT_URL.format(pk=exchange.pk),
        )
        assert response.status_code == HTTPStatus.OK
        exchange.refresh_from_db()
        assert exchange.status == ExchangeStatusChoices.REJECTED
