# -*- coding: utf-8 -*-
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.conf import settings
import os
import json
from datetime import date
from django.contrib.auth.models import User
from wechat_client.models import WeChat
import logging
logger = logging.getLogger(__name__)


def applogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = User.objects.filter(username=username).first()
            if not user:
                return JsonResponse({'msg': '用户名错误'}, status=401)
            if user.check_password(password):
                # 获取微信二维码
                data, info = WeChat.get_qr_code(user.id)
                if data:
                    return JsonResponse({"code": 0, "data": data, "msg": "success"})
                else:
                    return JsonResponse({"code": 0, "data": None, "msg": info}, status=403)
            return JsonResponse({"code": 0, "data": None, "msg": "密码错误"}, status=403)
        return JsonResponse({'msg': '请提供用户名和密码'}, status=403)
    else:
        return JsonResponse({'msg': '请求方法错误'}, status=403)


def checklogin(request):
    if request.method == 'GET':
        hwnd = request.GET.get('hwnd', '')
        wait = request.GET.get('wait', False)
        username = request.GET.get('username', '')
        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'msg': '用户名错误'}, status=401)
        data = WeChat.check_login(user.id, int(hwnd), wait)
        return JsonResponse({"code": 0, "data": data, "msg": "success"})
    else:
        return JsonResponse({'msg': '请求方法错误'}, status=403)


def wx_msg_receive(request, msg_type):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username', '')
            friends = data.get('friends', [])
            content = data.get('content', '')
        except:
            username = request.POST.get('username', '')
            friends = request.POST.get('friends', [])
            content = request.POST.get('content', '')
        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'msg': '用户名错误'}, status=401)

        if msg_type == 'file':
            pdf = request.FILES.get("pdf", None)
            friends = eval(friends)
            file_name = request.POST.get('file_name', '文件.pdf')
            pdf_path = os.path.join(settings.PDF_DIR, '{}'.format(date.today()))
            if not os.path.exists(pdf_path):
                os.makedirs(pdf_path, 0o777)
            content = os.path.join(pdf_path, file_name)
            with open(content, 'wb+') as f:  # 打开特定的文件进行二进制的写操作
                for chunk in pdf.chunks():  # 分块写入文件
                    f.write(chunk)
        if friends and content:
            online_wx, info = WeChat.get_online_wx(user.id)
            if not online_wx:
                print(info)
                return JsonResponse({'msg': info}, status=401)
            result = online_wx.send_msg(friends, content, msg_type=msg_type)
            if not result:
                online_wx.check_online_wx()
                print('您的微信账号尚未登入')
                return JsonResponse({'msg': '您的微信账号尚未登入'}, status=403)
        return JsonResponse({"code": 0, "data": None, "msg": "success"})
    return JsonResponse({'msg': '请求方法错误'}, status=403)


def test(request):
    if request.method == 'GET':
        result = 'eeee'
        return JsonResponse({"code": 0, "data": result, "msg": "success"})
    return JsonResponse({'msg': '请求方法错误'}, status=403)
