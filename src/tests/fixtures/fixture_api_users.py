import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_user_one(django_user_model):
    return django_user_model.objects.create_user(
        username="apiuser",
        password="apipassword",
        email="apiuser@user.com",
        first_name="API",
        last_name="User",
    )


@pytest.fixture
def api_user_one_token(api_user_one):
    token = AccessToken.for_user(api_user_one)
    return {
        "access": str(token),
    }


@pytest.fixture
def api_user_one_client(api_user_one_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {api_user_one_token['access']}"
    )
    return client


@pytest.fixture
def api_user_two(django_user_model):
    return django_user_model.objects.create_user(
        username="apiuser2",
        password="apipassword2",
        email="apiusertwo@two.ru",
        first_name="API2",
        last_name="User2",
    )


@pytest.fixture
def api_user_two_token(api_user_two):
    token = AccessToken.for_user(api_user_two)
    return {
        "access": str(token),
    }


@pytest.fixture
def api_user_two_client(api_user_two_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {api_user_two_token['access']}"
    )
    return client


@pytest.fixture
def api_user_three(django_user_model):
    return django_user_model.objects.create_user(
        username="apiuser3",
        password="apipassword3",
        first_name="API3",
        last_name="User3",
        email="some@sda.ru",
    )


@pytest.fixture
def api_user_three_token(api_user_three):
    token = AccessToken.for_user(api_user_three)
    return {
        "access": str(token),
    }


@pytest.fixture
def api_user_three_client(api_user_three_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {api_user_three_token['access']}"
    )
    return client
