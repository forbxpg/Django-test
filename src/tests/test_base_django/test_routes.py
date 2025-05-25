"""Модуль для тестирования маршрутов в Django."""

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
