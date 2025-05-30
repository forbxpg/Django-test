"""Формы для создания и редактирования пользователей."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from unfold.forms import UserCreationForm

from core import config


User = get_user_model()


class UserCreateForm(UserCreationForm):
    """Форма для создания нового пользователя."""

    phone = PhoneNumberField(
        label=_("Номер телефона (опционально)"),
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": _("Имя пользователя"),
                    "class": config.DEFAULT_CSS_CLASS,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("Email"),
                    "class": config.DEFAULT_CSS_CLASS,
                },
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": _("Номер телефона (опционально)"),
                    "class": config.DEFAULT_CSS_CLASS,
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": _("Имя"),
                    "class": config.DEFAULT_CSS_CLASS,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": _("Фамилия"),
                    "class": config.DEFAULT_CSS_CLASS,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы."""
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": _("Пароль"),
                "class": config.DEFAULT_CSS_CLASS,
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": _("Повторите пароль"),
                "class": config.DEFAULT_CSS_CLASS,
            }
        )
        self.fields["phone"].widget.attrs.update(
            {
                "placeholder": _("Номер телефона (опционально)"),
                "class": config.DEFAULT_CSS_CLASS,
            }
        )


class UserLoginForm(AuthenticationForm):
    """Форма для входа пользователя."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": _("Имя пользователя"),
                "class": config.DEFAULT_CSS_CLASS,
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": _("Пароль"),
                "class": config.DEFAULT_CSS_CLASS,
            }
        )


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": _("Имя пользова��еля"),
                    "class": config.DEFAULT_CSS_CLASS,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("Email"),
                    "class": config.DEFAULT_CSS_CLASS,
                },
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": _("Номер телефона (опционально)"),
                    "class": config.DEFAULT_CSS_CLASS,
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": _("Имя"),
                    "class": config.DEFAULT_CSS_CLASS,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": _("Фамилия"),
                    "class": config.DEFAULT_CSS_CLASS,
                },
            ),
        }
