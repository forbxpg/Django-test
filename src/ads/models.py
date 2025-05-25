"""Модуль для моделей приложения ads."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from core import config
from core.utils import AdConditionChoices


User = get_user_model()


class Ad(models.Model):
    """Модель объявления в базе данных."""

    title = models.CharField(
        max_length=config.AD_TITLE_LENGTH,
        verbose_name=_("Заголовок объявления"),
    )
    description = models.TextField(
        _("Описание объявления"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Автор объявления"),
    )
    image = models.ImageField(
        _("Изображение объявления"),
        blank=True,
        null=True,
    )
    condition = models.CharField(
        max_length=config.CONDITION_CHOICE_LENGTH,
        choices=AdConditionChoices.choices,
        default=AdConditionChoices.NEW,
        verbose_name=_("Состояние товара"),
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name=_("Категория объявления"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания объявления"),
    )
    is_exchanged = models.BooleanField(
        default=False,
        verbose_name=_("Обменено"),
    )

    class Meta:
        verbose_name = _("Объявление")
        verbose_name_plural = _("Объявления")
        ordering = ("-created_at",)
        default_related_name = "ads"
        indexes = [
            models.Index(fields=["user"], name="user_idx"),
            models.Index(fields=["category"], name="category_idx"),
        ]

    @property
    def condition_display(self):
        """Возвращает отображаемое состояние объявления."""
        return AdConditionChoices(self.condition).label

    def __str__(self):
        return _("Объявление: %(title)s пользователя %(user)s") % {
            "title": self.title,
            "user": self.user.username,
        }


class Category(models.Model):
    """Модель категорий объявлений."""

    name = models.CharField(
        _("Название категории"),
        max_length=config.CATEGORY_TITLE_LENGTH,
    )
    slug = models.SlugField(
        _("Уникальный идентификатор категории"),
        max_length=config.CATEGORY_SLUG_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = _("Категория объявления")
        verbose_name_plural = _("Категории объявлений")
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                self.slug = str(self.name) + get_random_string(
                    config.CATEGORY_SLUG_LENGTH,
                )
                if not Category.objects.filter(slug=self.slug).exists():
                    break
        return super().save(*args, **kwargs)

    def __str__(self):
        return _("Категория: %(name)s") % {
            "name": self.name,
        }
