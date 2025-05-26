from http import HTTPStatus

import pytest

from django.urls import reverse

from core.utils import ExchangeStatusChoices
from exchanges.models import ExchangeProposal
from tests.fixtures.fixture_base_users import user_three


@pytest.mark.django_db(transaction=True)
class TestBaseDjangoExchanges:

    EXCHANGE_LIST = reverse("exchanges:exchanges-list")
    EXCHANGE_CREATE = reverse("exchanges:create-exchange")

    def test_exchange_list_no_auth(self, client):
        response = client.get(self.EXCHANGE_LIST)
        assert response.status_code == HTTPStatus.FOUND
        assert "/users/login/?next=/exchanges/" in response.url

    def test_exchange_list_with_auth(self, user_one_client, exchange_base):
        response = user_one_client.get(self.EXCHANGE_LIST)
        assert response.status_code == HTTPStatus.OK
        assert response.context["page_obj"].object_list == [exchange_base]

    def test_exchange_list_objects_for_different_users(
        self,
        user_one_client,
        user_two_client,
        ad_two,
        ad_three,
        user_three_client,
    ):
        ExchangeProposal.objects.create(
            ad_sender=ad_two,
            ad_receiver=ad_three,
            status="accepted",
        )
        response = user_one_client.get(self.EXCHANGE_LIST)
        response_user_two = user_two_client.get(self.EXCHANGE_LIST)
        response_user_three = user_three_client.get(self.EXCHANGE_LIST)
        assert response.status_code == HTTPStatus.OK
        assert response_user_two.status_code == HTTPStatus.OK
        assert response_user_three.status_code == HTTPStatus.OK
        assert len(response.context["page_obj"]) == 1
        assert len(response_user_two.context["page_obj"]) == 1
        assert len(response_user_three.context["page_obj"]) == 0

    def test_exchange_detail_no_auth(self, client, exchange_base):
        response = client.get(
            reverse(
                "exchanges:exchange-detail",
                kwargs={"proposal_id": exchange_base.id},
            )
        )
        assert response.status_code == HTTPStatus.FOUND
        assert "/users/login/?next=/exchanges/" in response.url

    def test_exchange_detail_with_auth(
        self,
        user_one_client,
        exchange_base,
        ad_one,
    ):
        response = user_one_client.get(
            reverse(
                "exchanges:exchange-detail",
                kwargs={"proposal_id": exchange_base.id},
            )
        )
        assert response.status_code == HTTPStatus.OK
        assert response.context["proposal"] == exchange_base
        assert response.context["proposal"].ad_sender.user == ad_one.user

    def test_exchange_detail_not_participant(
        self,
        user_three_client,
        exchange_base,
    ):
        response = user_three_client.get(
            reverse(
                "exchanges:exchange-detail",
                kwargs={"proposal_id": exchange_base.id},
            )
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_exchange_create_no_auth(self, client):
        response = client.get(self.EXCHANGE_CREATE)
        assert response.status_code == HTTPStatus.FOUND
        assert "/users/login/?next=/exchanges/create/" in response.url

    def test_exchange_create_with_auth(
        self,
        user_one_client,
        ad_two,
        ad_three,
    ):
        data = {
            "ad_sender": ad_two.id,
            "ad_receiver": ad_three.id,
            "comment": "some comm",
        }
        response = user_one_client.post(self.EXCHANGE_CREATE, data=data)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == self.EXCHANGE_LIST
        assert ExchangeProposal.objects.count() == 1
        exchange = ExchangeProposal.objects.first()
        assert exchange.ad_sender == ad_two
        assert exchange.ad_receiver == ad_three
        assert exchange.status == ExchangeStatusChoices.PENDING

    def test_exchange_create_with_auth_same_user(
        self,
        user_one_client,
        ad_two,
        ad_one,
    ):
        data = {
            "ad_sender": ad_two.id,
            "ad_receiver": ad_one.id,
            "comment": "some comm",
        }
        response = user_one_client.post(self.EXCHANGE_CREATE, data=data)
        assert ExchangeProposal.objects.count() == 0

    def test_exchange_create_already_exchanged_ads(
        self,
        exchange_base,
        ad_two,
        ad_three,
        user_one_client,
    ):
        response = user_one_client.post(
            self.EXCHANGE_CREATE,
            data={
                "ad_sender": ad_two.id,
                "ad_receiver": ad_three.id,
                "comment": "some comm",
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert ExchangeProposal.objects.count() == 1

    def test_exchange_create_unique_together(
        self,
        user_one_client,
        ad_two,
        ad_three,
    ):
        ExchangeProposal.objects.create(
            ad_sender=ad_two,
            ad_receiver=ad_three,
            status=ExchangeStatusChoices.PENDING,
        )
        response = user_one_client.post(
            self.EXCHANGE_CREATE,
            data={
                "ad_sender": ad_two.id,
                "ad_receiver": ad_three.id,
                "comment": "some comm",
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert ExchangeProposal.objects.count() == 1

    def test_exchange_create_invalid_ads(
        self,
        user_one_client,
        ad_two,
    ):
        response = user_one_client.post(
            self.EXCHANGE_CREATE,
            data={
                "ad_sender": ad_two.id,
                "ad_receiver": "",
                "comment": "some comm",
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert ExchangeProposal.objects.count() == 0

    def test_status_change_form(
        self,
        user_one_client,
        exchange_base_two,
    ):
        data = {
            "status": ExchangeStatusChoices.REJECTED,
        }
        response = user_one_client.post(
            reverse(
                "exchanges:exchange-detail",
                kwargs={"proposal_id": exchange_base_two.id},
            ),
            data=data,
        )
        assert response.status_code == HTTPStatus.FOUND
        exchange_base_two.refresh_from_db()
        assert exchange_base_two.status == ExchangeStatusChoices.REJECTED

    def test_status_change_form_not_participant(
        self,
        user_two_client,
        exchange_base_two,
    ):
        data = {
            "status": ExchangeStatusChoices.ACCEPTED,
        }
        response = user_two_client.post(
            reverse(
                "exchanges:exchange-detail",
                kwargs={"proposal_id": exchange_base_two.id},
            ),
            data=data,
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        exchange_base_two.refresh_from_db()
        assert exchange_base_two.status == ExchangeStatusChoices.PENDING
