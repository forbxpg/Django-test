from http import HTTPStatus

import pytest

from django.urls import reverse

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
