from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def user_register_view(request):
    """Отображает страницу регистрации."""
    return render(
        request,
        "users/register.html",
        {},
    )


def user_login_view(request):
    """Отображает страницу входа в систему."""
    return render(
        request,
        "users/login.html",
        {},
    )


@login_required
def user_logout_view(request):
    """Отображает страницу выхода из системы."""
    return render(
        request,
        "users/logout.html",
        {},
    )
