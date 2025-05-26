import pytest

from ads.models import Ad, Category


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
        title="Test ad obj",
        description="Test desc",
        user=api_user_one,
        category=api_category,
    )
