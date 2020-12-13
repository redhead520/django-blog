from django.contrib import admin
from wechat_client.models import WeChat


@admin.register(WeChat)
class WeChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'wx_account', 'online', 'active')
    list_display_links = ('id', 'user', 'wx_account')
