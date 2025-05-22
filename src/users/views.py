from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls.base import reverse

from .forms import UserCreateForm, UserLoginForm


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


def user_profile_view(request):
    """Отображает страницу профиля пользователя."""
    user = get_user_model()
    return render(
        request,
        "users/profile.html",
        {"user": user},
    )
