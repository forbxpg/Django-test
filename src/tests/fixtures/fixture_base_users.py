import pytest
from django.test import Client


@pytest.fixture
def auth_user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="testpassword",
        email="test@test.com",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def auth_user_client(auth_user):
    client = Client()
    client.force_login(auth_user)
    return client


@pytest.fixture
def ad_user_one(django_user_model):
    return django_user_model.objects.create_user(
        username="aduser",
        password="adpassword",
        email="ademail@em.com",
        first_name="Ad",
        last_name="User",
    )


@pytest.fixture
def ad_user_client(ad_user_one):
    client = Client()
    client.force_login(ad_user_one)
    return client


@pytest.fixture
def ad_user_two(django_user_model):
    return django_user_model.objects.create_user(
        username="aduser2",
        password="adpassword2",
        email="aduser2@em.com",
        first_name="Ad2",
        last_name="User2",
    )
