from http import HTTPStatus

import pytest

from django.urls import reverse
from ads.models import Ad, Category
from exchanges.models import ExchangeProposal


@pytest.mark.django_db(transaction=True)
class TestBaseDjangoAds:

    ADS_LIST = reverse("ads:ads-list")

    def test_ads_list_no_auth(self, client, ad_one):
        response = client.get(self.ADS_LIST)
        assert response.status_code == HTTPStatus.OK
        assert response.context["page_obj"].object_list == [ad_one]
        assert "filter" in response.context
