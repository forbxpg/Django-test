from django.urls import path


from . import views


app_name = "users"

urlpatterns = [
    path("register/", views.user_register_view, name="register"),
]
