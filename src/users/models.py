"""Модель пользователя в базе данных."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core import config


class User(AbstractUser):
    """Модель пользователя в БД."""

    first_name = models.CharField(
        _("Имя"),
        max_length=config.USER_NAME_LENGTH,
    )
    last_name = models.CharField(
        _("Фамилия"),
        max_length=config.USER_NAME_LENGTH,
    )
    email = models.EmailField(
        _("Адрес электронной почты"),
        unique=True,
    )
    phone = PhoneNumberField(
        _("Номер телефона"),
        blank=True,
        null=True,
        region=config.PHONE_REGION,
        unique=True,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("username",)

    def __str__(self):
        return _("Пользователь: %(username)s") % {
            "username": self.username,
        }
