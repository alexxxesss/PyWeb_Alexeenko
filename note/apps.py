from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'note'

    verbose_name = _("Дела")
