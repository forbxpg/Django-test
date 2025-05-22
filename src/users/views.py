from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls.base import reverse

from .forms import UserCreateForm


def user_register_view(request):
    """Отображает страницу регистрации."""
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("ads:ad-list"))
    else:
        form = UserCreateForm()
    return render(
        request,
        "users/create.html",
        {"form": form},
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
