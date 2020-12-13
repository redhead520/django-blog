# -*- coding: utf-8 -*-

__author__ = 'Afa'

from wechat_client import views
from django.urls import path

urlpatterns = [
    path('login/wx', views.applogin, name='app_login'),
    path('check/login/wx', views.checklogin, name='check_login'),
    path('send/msg/<str:msg_type>', views.wx_msg_receive, name='app_receive_msg'),
    path('api/test', views.test, name='api_test'),
]

