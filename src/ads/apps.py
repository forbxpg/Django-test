from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ads"
    verbose_name = _("Управление объявлениями")

    def ready(self):
        """Метод, вызываемый при запуске приложения.
        Включает триггер для сигналов.
        """
        import ads.signals  # noqa: F401
