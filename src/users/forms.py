"""Формы для создания и редактирования пользователей."""

from django import forms

from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateForm(forms.ModelForm):
    """Форма для создания нового пользователя."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Фамилия"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Пароль"}),
        }


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
