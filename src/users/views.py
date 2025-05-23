from urllib import request

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from django.shortcuts import render, redirect

from .forms import UserCreateForm, UserProfileForm


User = get_user_model()


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


@login_required(login_url="users:login")
def user_profile_view(request):
    """Отображает страницу профиля."""
    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect(reverse("users:profile"))
    else:
        form = UserProfileForm(
            instance=request.user,
        )
    return render(
        request,
        "users/profile.html",
        {"form": form},
    )
