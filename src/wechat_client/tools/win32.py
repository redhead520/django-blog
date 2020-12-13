# -*- coding: utf-8 -*-
import win32gui
import win32con
import win32api
import time
from PIL import ImageGrab, Image
import os, sys
import autopy
import random
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
# import pyautogui


def gbk2utf8(s):
    try:
        return s.decode('gbk').encode('utf-8')
    except:
        return s


def _get_class_name(hwnd):
    name = win32gui.GetClassName(hwnd)
    return gbk2utf8(name)


def _get_title_name(hwnd):
    name = win32gui.GetWindowText(hwnd)
    return gbk2utf8(name)


def get_all_hwnds(class_name=None, title=None, fuzzy=False):
    """
    获取所有窗口的句柄
    :param class_name: 类名过滤
    :param title: 标题过滤
    :param fuzzy: 是否模糊过滤
    :return:
    """
    hwnd_list = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnd_list)

    if class_name:
        if fuzzy:
            hwnd_list = list(filter(lambda r: class_name in _get_class_name(r), hwnd_list))
        else:
            hwnd_list = list(filter(lambda r: _get_class_name(r) == class_name, hwnd_list))
    if title:
        if fuzzy:
            hwnd_list = list(filter(lambda r: title in _get_title_name(r), hwnd_list))
        else:
            hwnd_list = list(filter(lambda r: _get_title_name(r) == title, hwnd_list))
    return hwnd_list


def get_window_rect(hwnd):
    """窗口位置信息"""
    return win32gui.GetWindowRect(hwnd)


def is_window(hwnd):
    """是否是窗口句柄，句柄是否存在"""
    if isinstance(hwnd, str):
        hwnd = int(hwnd)
    return True if win32gui.IsWindow(hwnd) else False


def active_window(hwnd):
    rect = win32gui.GetWindowRect(hwnd)  # 窗口位置信息
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, rect[2] - rect[0], rect[3] - rect[1],
                          win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)
    time.sleep(0.1)
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, rect[2] - rect[0], rect[3] - rect[1],
                          win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)
    time.sleep(0.2)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except:
        print('Set Foreground Window Error!!!!!!!!![ 1st time]')
        time.sleep(5)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, rect[2] - rect[0], rect[3] - rect[1],
                              win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)
        time.sleep(0.1)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, rect[2] - rect[0], rect[3] - rect[1],
                              win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)
        time.sleep(0.2)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except:
            print('Set Foreground Window Error!!!!!!!!![ 2nd time]')



def move2(hwnd, x, y, active=True):
    """
    移动到窗口的相对位置x,y
    :param hwnd: 窗口句柄
    :param x: 窗口的相对位置 x
    :param y: 窗口的相对位置 y
    :return:
    """
    rect = win32gui.GetWindowRect(hwnd)  # 窗口位置信息
    if active:
        active_window(hwnd)
    # print(random.random()/2)
    time.sleep(0.1)        # 0-0.5s
    autopy.mouse.move(rect[0] + x, rect[1] + y)
    time.sleep(random.random()/6)        # 0-0.5s
    autopy.mouse.smooth_move(rect[0] + x, rect[1] + y)


def move(x, y):
    """
    移动到屏幕位置x,y
    :param x: 屏幕的相对位置 x
    :param y: 屏幕的相对位置 y
    :return:
    """
    autopy.mouse.move(x, y)
    time.sleep(random.random()/6)        # 0-0.5s
    autopy.mouse.smooth_move(x, y)


def paste_text(text):
    if not isinstance(text, str):
        text = str(text)
    if text.count('\n'):
        for i, t in enumerate(text.split('\n')):
            if i != 0 and t:
                autopy.key.tap(autopy.key.Code.RETURN, modifiers=[autopy.key.Modifier.SHIFT])
            autopy.key.type_string(t)
    else:
        autopy.key.type_string(text)


def click(num=1):
    time.sleep(random.random() / 4)  # 0-0.5s
    autopy.mouse.click()
    if num > 1:
        time.sleep(0.2)
        autopy.mouse.click()


key_mapping = {
    'ENTER': 'RETURN',
    'BACK': 'BACKSPACE',
    'ESC': 'ESCAPE'
}


def key(k, func=[]):
    if len(k) > 1:
        k = k.upper()
        k = key_mapping.get(k, k)
        k = getattr(autopy.key.Code, k)
    autopy.key.tap(k, modifiers=[getattr(autopy.key.Modifier, f.upper()) for f in func])

def ctrl_c():
    win32api.keybd_event(17,0,0,0)
    time.sleep(0.1)
    win32api.keybd_event(67,0,0,0)
    time.sleep(0.1)
    win32api.keybd_event(67,0,win32con.KEYEVENTF_KEYUP,0) 
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)

def screen_hwnd_shot(hwnd, name=None, temp_dir=None, is_img=False):
    """截图：截取句柄对应的窗口的图片,忽律遮盖的窗口"""
    if not name:
        name = 'img-{}'.format(hwnd)
    if not temp_dir:
        temp_dir = os.path.abspath('.')
    out_dir = os.path.join(temp_dir, '{}.jpg'.format(name))
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    if is_img:
        return img
    img.save(out_dir)
    return out_dir


def screen_shot(hwnd, name=None, x1=None, y1=None, x2=None, y2=None, temp_dir=None, is_img=False):
    """截图：截取句柄对应的窗口的图片"""
    if not name:
        name = 'img-{}'.format(hwnd)
    if not temp_dir:
        temp_dir = os.path.abspath('.')
    rect = win32gui.GetWindowRect(hwnd)
    out_dir = os.path.join(temp_dir, '{}.jpg'.format(name))
    x, y, w, h = rect[0], rect[1], rect[2]-rect[0], rect[3]-rect[1]
    if x1 or x2 or y1 or y2:
        x, y, w, h = x + x1, y + y1, x2-x1, y2-y1
    # img = pyautogui.screenshot(region=[x, y, w, h])  # x,y,w,h
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    img.save(out_dir)
    return img if is_img else out_dir

def ocr_recognize(image_dir, out_dir, lang='chi_sim'):
    command = 'tesseract {} {} -l {}'.format(image_dir, out_dir, lang)
    print(command)
    result = os.popen(command).read()
    print(result.decode('utf-8'))




