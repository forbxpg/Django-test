from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from unfold.admin import ModelAdmin


CustomUser = get_user_model()

admin.site.unregister(Group)


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "username",
        "email",
        "phone",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
