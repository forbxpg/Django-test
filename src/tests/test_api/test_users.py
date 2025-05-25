"""Тесты для API пользователей."""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestDjoserUserAPI:

    REGISTER_URL = "/api/v1/users/"
    TOKEN_URL = "/api/v1/auth/jwt/create/"
    ME_URL = "/api/v1/users/me/"
    TEST_DATA = {
        "username": "testuser",
        "password": "someeepaswds900",
        "email": "adm@jj.com",
        "first_name": "Test",
        "last_name": "User",
    }

    def test_user_register(self, api_client):
        response = api_client.post(
            self.REGISTER_URL, data=self.TEST_DATA, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == self.TEST_DATA["username"]
        assert response.data["email"] == self.TEST_DATA["email"]

    def test_user_get_token(self, api_user_one_client, api_user_one):
        response = api_user_one_client.post(
            self.TOKEN_URL,
            data={
                "username": api_user_one.username,
                "password": "apipassword",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_user_get_token_invalid_credentials(self, api_user_one_client):
        response = api_user_one_client.post(
            self.TOKEN_URL,
            data={
                "username": "invaliduser",
                "password": "wrongpassword",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_get_me(self, api_user_one_client, api_user_one):
        response = api_user_one_client.get(self.ME_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == api_user_one.username

    def test_user_get_me_unauthenticated(self, api_client):
        response = api_client.get(self.ME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_update_me(self, api_user_one_client, api_user_one):
        updated_data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = api_user_one_client.patch(
            self.ME_URL, data=updated_data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == updated_data["first_name"]
        assert response.data["last_name"] == updated_data["last_name"]

    def test_user_update_me_unauthenticated(self, api_client):
        updated_data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = api_client.patch(
            self.ME_URL, data=updated_data, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
