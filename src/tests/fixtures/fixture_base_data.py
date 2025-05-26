import pytest
from django.urls import reverse

from ads.models import Ad, Category
from core.utils import ExchangeStatusChoices
from exchanges.models import ExchangeProposal
from tests.fixtures.fixture_base_users import user_one, user_two


@pytest.fixture
def category_one(db):
    return Category.objects.create(
        name="Category One",
        slug="category-one",
    )


@pytest.fixture
def category_two(db):
    return Category.objects.create(
        name="Category Two",
        slug="category-two",
    )


@pytest.fixture
def ad_one(db, category_one, user_one):
    return Ad.objects.create(
        title="Ad One",
        description="Description for Ad One",
        category=category_one,
        user=user_one,
    )


@pytest.fixture
def ad_two(db, category_one, user_one):
    return Ad.objects.create(
        title="Ad Two",
        description="Description for Ad Two",
        category=category_one,
        user=user_one,
    )


@pytest.fixture
def ad_three(db, category_two, user_two):
    return Ad.objects.create(
        title="Ad Three",
        description="Description for Ad Three",
        category=category_two,
        user=user_two,
    )


@pytest.fixture
def exchange_base(db, ad_one, ad_three):
    return ExchangeProposal.objects.create(
        ad_sender=ad_one,
        ad_receiver=ad_three,
        status=ExchangeStatusChoices.ACCEPTED,
    )


@pytest.fixture
def ad_four(db, category_two, user_three):
    return Ad.objects.create(
        title="Ad Four",
        description="Description for Ad Four",
        category=category_two,
        user=user_three,
    )


@pytest.fixture
def exchange_base_two(db, ad_two, ad_four):
    return ExchangeProposal.objects.create(
        ad_sender=ad_four,
        ad_receiver=ad_two,
        status=ExchangeStatusChoices.PENDING,
    )
