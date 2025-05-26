import pytest

from ads.models import Ad, Category
from core.utils import ExchangeStatusChoices
from exchanges.models import ExchangeProposal


@pytest.fixture
def api_category(db):
    return Category.objects.create(
        name="Test Category",
        slug="test-category",
    )


@pytest.fixture
def api_category_two(db):
    return Category.objects.create(
        name="Test Category Two",
        slug="test-category-two",
    )


@pytest.fixture
def api_ad_one(db, api_user_one, api_category):
    return Ad.objects.create(
        title="Test Ad One",
        description="This is a test ad one.",
        user=api_user_one,
        category=api_category,
    )


@pytest.fixture
def api_ad_two(db, api_user_one, api_category_two):
    return Ad.objects.create(
        title="Test Ad Two",
        description="This is a test ad two.",
        user=api_user_one,
        category=api_category_two,
    )


@pytest.fixture
def api_ad_three(db, api_user_two, api_category):
    return Ad.objects.create(
        title="Test Ad Three",
        description="This is a test ad three.",
        user=api_user_two,
        category=api_category,
    )


@pytest.fixture
def api_accepted_exchange(db, api_ad_one, api_ad_three, api_user_three):
    return ExchangeProposal.objects.create(
        ad_sender=api_ad_one,
        ad_receiver=api_ad_three,
        comment="Test exchange proposal",
        status=ExchangeStatusChoices.ACCEPTED,
    )
