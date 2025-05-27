"""Админка для модели объявлений."""

from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Ad, Category


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """Админка для категорий."""

    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ad)
class AdAdmin(ModelAdmin):
    ...
