"""Формы для создания и редактирования пользователей."""

from django import forms
from django.contrib.auth import get_user_model
from unfold.forms import UserCreationForm

from core import config


User = get_user_model()


class UserCreateForm(UserCreationForm):
    """Форма для создания нового пользователя."""

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
                attrs={"placeholder": "Имя пользователя", "class": config.TITLE_CLASS}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": config.TITLE_CLASS}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "Телефон", "class": config.TITLE_CLASS}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": "Имя", "class": config.TITLE_CLASS}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Фамилия", "class": config.TITLE_CLASS}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы."""
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Пароль",
                "class": config.TITLE_CLASS,
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Повторите пароль",
                "class": config.TITLE_CLASS,
            }
        )


class UserUpdateForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Фамилия"}),
        }
