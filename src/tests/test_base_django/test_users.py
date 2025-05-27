from http import HTTPStatus

from django.contrib.auth import get_user_model
import pytest

from django.urls import reverse


User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestBaseDjangoUsers:

    LOGIN_URL = reverse("users:login")
    LOGOUT_URL = reverse("users:logout")
    REGISTER_URL = reverse("users:register")
    PROFILE_URL = reverse("users:profile")

    def test_login_page(self, client):
        response = client.get(self.LOGIN_URL)
        assert response.status_code == HTTPStatus.OK

    def test_logout_page(self, client):
        response = client.get(self.LOGOUT_URL)
        assert response.status_code == HTTPStatus.FOUND

    def test_register_page(self, client):
        response = client.get(self.REGISTER_URL)
        assert response.status_code == HTTPStatus.OK
        assert "form" in response.context
        assert response.context["form"].is_bound is False

    def test_user_login(self, user_one_client, user_one):
        response = user_one_client.post(
            self.LOGIN_URL,
            data={
                "username": user_one.username,
                "password": "apipassword",
            },
        )
        assert response.status_code == HTTPStatus.OK

    def test_user_logout(self, user_one_client, user_one):
        response = user_one_client.post(self.LOGOUT_URL)
        assert response.status_code == HTTPStatus.FOUND
        response = user_one_client.post(self.PROFILE_URL)
        assert response.status_code == HTTPStatus.FOUND
        assert "/users/login/?next=/users/profile/" in response.url

    def test_user_register(self, client):
        response = client.post(
            self.REGISTER_URL,
            data={
                "username": "newuser",
                "password1": "newpassword1",
                "password2": "newpassword1",
                "email": "dsadsa@dsads.ru",
                "first_name": "New",
                "last_name": "User",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("ads:ads-list")
        assert User.objects.count() == 1
