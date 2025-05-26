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


