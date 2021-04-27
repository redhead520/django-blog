from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NovelConfig(AppConfig):
    name = 'novel'

    verbose_name = _("小说")
    orderIndex = 5
