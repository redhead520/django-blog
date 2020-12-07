from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = _("博客")
    orderIndex = 1
