import pytest
from django.urls import reverse

from ads.models import Ad, Category
from exchanges.models import ExchangeProposal


@pytest.fixture
def category(db):
    from ads.models import Category

    return Category.objects.create(
        name="Test Category",
        slug="test-category",
    )


@pytest.fixture
def ad_one(db, ad_user_one):
    from ads.models import Ad

    return Ad.objects.create(
        title="Test ad obj",
        description="Test desc",
        user=ad_user_one,
    )


@pytest.fixture
def ad_two(db, ad_user_two):
    from ads.models import Ad

    return Ad.objects.create(
        title="Test ad obj 2",
        description="Test desc 2",
        user=ad_user_two,
    )


@pytest.fixture
def exchange_proposal(db, ad_one, ad_two):
    from exchanges.models import ExchangeProposal

    return ExchangeProposal.objects.create(
        ad_sender=ad_one, ad_receiver=ad_two
    )
