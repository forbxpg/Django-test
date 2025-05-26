import pytest
from django.test import Client


@pytest.fixture
def user_one(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="testpassword",
        email="test@test.com",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def user_one_client(user_one):
    client = Client()
    client.force_login(user_one)
    return client


@pytest.fixture
def user_two(django_user_model):
    return django_user_model.objects.create_user(
        username="aduser2",
        password="adpassword2",
        email="aduser2@em.com",
        first_name="Ad2",
        last_name="User2",
    )


@pytest.fixture
def user_two_client(user_two):
    client = Client()
    client.force_login(user_two)
    return client


@pytest.fixture
def user_three(django_user_model):
    return django_user_model.objects.create_user(
        username="aduser3",
        password="adpassword3",
        email="somdasknd@email.com",
        first_name="Ad3",
        last_name="User3",
    )


@pytest.fixture
def user_three_client(user_three):
    client = Client()
    client.force_login(user_three)
    return client
