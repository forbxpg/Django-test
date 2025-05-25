"""Модуль для фикстур тестов API и базового Django приложения."""

from django.urls import reverse
import pytest
from pytest_lazyfixture import lazy_fixture


# Base Django fixtures
@pytest.fixture
def login_url():
    ...

