import pytest
from django.urls import reverse

from ads.models import Ad, Category
from exchanges.models import ExchangeProposal
from tests.fixtures.fixture_base_users import user_one, user_two


@pytest.fixture
def category_one():
    return Category.objects.create(
        name="Category One",
        slug="category-one",
    )


@pytest.fixture
def category_two():
    return Category.objects.create(
        name="Category Two",
        slug="category-two",
    )


@pytest.fixture
def ad_one(category_one, user_one):
    return Ad.objects.create(
        title="Ad One",
        description="Description for Ad One",
        category=category_one,
        user=user_one,
    )


@pytest.fixture
def ad_two(category_one, user_one):
    return Ad.objects.create(
        title="Ad Two",
        description="Description for Ad Two",
        category=category_one,
        user=user_one,
    )


@pytest.fixture
def ad_three(category_two, user_two):
    return Ad.objects.create(
        title="Ad Three",
        description="Description for Ad Three",
        category=category_two,
        user=user_two,
    )


