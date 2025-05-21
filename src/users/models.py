"""Модуль для определения модели пользователя проекта."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя приложения."""

    first_name = models.CharField(
        _("Имя пользователя"),
        max_length=150,
    )
    email = models.EmailField(
        _("Адрес электронной почты"),
        unique=True,
        db_index=True,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name"]



