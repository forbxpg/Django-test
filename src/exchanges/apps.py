from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExchangesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exchanges"
    verbose_name = _("Управлениями предложениями обмена")
