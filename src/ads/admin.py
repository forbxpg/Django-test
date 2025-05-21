from django.contrib import admin

from .models import Ad, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""

    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    ...