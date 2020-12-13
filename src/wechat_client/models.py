# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from wechat_client import weclient
import os


class WeChat(models.Model):
    user = models.ForeignKey(User, verbose_name='登入账号', on_delete=models.CASCADE, blank=False)
    wx_account = models.CharField('微信账号', blank=False, max_length=50)
    # account_path = models.FilePathField(path='./wechat_client/static/image/account', verbose_name='账号图片地址', max_length=100, blank=True)
    online = models.BooleanField('是否已登入', default=False, blank=False)
    active = models.BooleanField('是否启用', default=True, blank=False)

    def __str__(self):
        return '{}[{}]'.format(self.user.username, self.wx_account)

    class Meta:
        ordering = ['user', 'wx_account']
        verbose_name = "微信账号"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    @classmethod
    def get_online_wx(cls, user_id):
        online_wx = cls.objects.filter(user=user_id, online=True).first()
        if online_wx:
            if weclient.check_account(online_wx.wx_account):
                return online_wx, 'success'
            else:
                online_wx.online = False
                online_wx.save()                
        wxs = WeChat.objects.filter(user=user_id)
        for outline_wx in wxs:        
            if weclient.check_account(outline_wx.wx_account):
                outline_wx.online = True
                outline_wx.save() 
                return outline_wx, 'success'
        return None, '您的微信账号尚未登入!' if wxs else '您尚未有用账户，请联系工作人员!'

    @classmethod
    def get_qr_code(cls, user_id):
        url = ''
        online_wx = cls.objects.filter(user=user_id, online=True).first()
        if online_wx and cls.check_online_wx(user_id):          
            return None, '你的微信已经登入了'
        else:
            outline_wx = cls.objects.filter(user=user_id, online=False).first()
            if outline_wx and cls.check_online_wx(user_id):          
                return None, '你的微信已经登入了'
        data = weclient.login()
        if data:
            url = '/static/image/temp/' + os.path.split(data['url'])[1]
            data.update({'url': url})
            return data, 'success'
        return url, '服务器无法登入微信，请联系管理员!'

    def send_msg(self, friends, content, msg_type='text'):
        for friend in friends:
            weclient.send_msg(self.wx_account, friend, content, msg_type)
        return True

    @classmethod
    def check_login(cls, user_id, hwnd, wait=False):
        is_login = weclient.check_login(hwnd, wait=wait)
        if is_login:
            cls.check_online_wx(user_id)
            return True
        return False

    @classmethod
    def check_online_wx(cls, user_id=None):
        result = None
        account_mapping = weclient.get_account_list()
        for on in cls.objects.filter(online=True):
            if on.wx_account not in account_mapping:
                on.online = False
                on.save()
            else:
                account_mapping.pop(on.wx_account)
                if on.user.id == user_id:
                    result = on
        for account, kwnd in account_mapping.items():
            wx_account = cls.objects.filter(wx_account=account).first()
            if not wx_account:
                weclient.login()
            else:
                if not wx_account.online:
                    wx_account.online = True
                    # wx_account.account_path = '{}.jpg'.format(account)
                    wx_account.save()
                if wx_account.user.id == user_id:
                    result = wx_account
        return result

