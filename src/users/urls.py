"""Маршрутизация приложения users."""

from django.contrib.auth.views import LogoutView
from django.urls import path

from .forms import UserLoginForm


from . import views


app_name = "users"

urlpatterns = [
    path("register/", views.user_register_view, name="register"),
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            form_class=UserLoginForm,
        ),
        name="login",
    ),
    path(
        "logout/", LogoutView.as_view(next_page="ads:ads-list"), name="logout"
    ),
    path("profile/", views.user_profile_view, name="profile"),
]
