from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WxConfig(AppConfig):
    name = 'wechat_client'
    verbose_name = _("微信客户端")
