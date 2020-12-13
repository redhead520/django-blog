
import time, os, sys
import threading
import queue
from .tools import win32, img
import shutil
import os
import uuid
import random
from datetime import date
from pprint import pprint
import pyperclip

Task_Queue = queue.Queue()
Result_Queue = queue.Queue()
task_timeout = 30    #


class TaskWork(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='api_task')
        self._task = None
        self.task_list = Task_Queue
        self.result_list = Result_Queue

    def run(self):
        while True:
            self._task = self.task_list.get()
            print('{0}处理{1}级任务： {2}'.format(time.strftime("%Y-%m-%d %X"), self._task.priority, self._task.name))
            try:
                self._task.result = self._task.func()
                if self._task.wait:
                    self.result_list.put(self._task)
            except Exception as e:
                if self._task.wait:
                    self._task.error = e.args[0]
                    self.result_list.put(self._task)
            # Task_Queue.put(_task)
            time.sleep(0.5)


class Task(object):
    def __init__(self, id, priority, func, wait=True, name=''):
        self.id = id
        self.name = name
        self.priority = priority
        self.func = func
        self.result = None
        self.error = None
        self.wait = wait


task_work = TaskWork()
task_work.setDaemon(True)
task_work.start()


def task(priority=10, wait=True, name=''):
    def decorator(func):
        def wrapper(*args, **kw):
            start = time.time()
            id = '{}-{}'.format(uuid.uuid1(), random.random()*1000)
            Task_Queue.put(Task(id, priority, lambda: func(*args, **kw), wait=wait, name=name))
            while wait:
                _task = Result_Queue.get()
                if _task.id == id:
                    return _task.result
                Result_Queue.put(_task)
                if time.time() - start > task_timeout:
                    return False
                time.sleep(0.5)
            return True
        return wrapper
    return decorator


class WechatClient(object):
    def __init__(self):
        self.title = '微信'
        self.login_class = 'WeChatLoginWndForPC'   #  280x400
        self.tip_class = 'AlertDialog'
        self.body_class = 'WeChatMainWndForPC'  #  851x500
        self.search_icon = os.path.join(os.path.dirname(__file__), 'static', 'image', 'search_icon.jpg')
        self.temp_dir = os.path.join(os.path.dirname(__file__), 'static', 'image', 'temp')
        self.account_dir = os.path.join(os.path.dirname(__file__), 'static', 'image', 'account')
        self.pdf_dir = os.path.join(os.path.dirname(__file__), 'static', 'pdf')
        self.all_account = {}
        self.send_count = 0   # 发送消息次数
        self.clear_logout_tips()
        # self.get_account_list()

    def clear_logout_tips(self, sleep=4.0):
        time.sleep(sleep)
        for h in win32.get_all_hwnds(self.tip_class, self.title):
            win32.move2(h, 180, 188)
            win32.click()

    def clear_hot_key_tips(self, sleep=2.0):
        time.sleep(sleep)
        for h in win32.get_all_hwnds('ConfirmDialog', '热键冲突'):
            win32.move2(h, 244, 188)
            win32.click()

    def clear_open_file_window(self, sleep=1.0):
        time.sleep(sleep)
        for h in win32.get_all_hwnds('#', '打开', fuzzy=True):
            win32.key('ESC')
            time.sleep(0.2)

    def login(self):
        login_hwnds = win32.get_all_hwnds(self.login_class, None)
        if login_hwnds:
            hwnd = login_hwnds[0]
            self.clear_logout_tips(0.3)
            win32.move2(hwnd, 140, 352)
            win32.click()
            # 截取登入二维码
            time.sleep(0.2)
            img_dir = win32.screen_shot(hwnd, x1=2, y1=30, x2=278, y2=370,temp_dir=self.temp_dir)
            return {'hwnd': hwnd, 'url': img_dir}
        return False

    def check_login(self, hwnd, wait=False):
        if not wait:
            return not win32.is_window(hwnd)
        for i in range(20):
            if win32.is_window(hwnd):
                time.sleep(1)
            else:
                return True
        return False

    def loginout(self, hwnd):
        if win32.is_window(hwnd):
            r = win32.get_window_rect(hwnd)  # 窗口位置信息
            win32.move2(hwnd, 30, r[3] - r[1] - 24)
            win32.click()
            time.sleep(0.2)
            win32.move2(hwnd, 120, r[3] - r[1] - 35, False)
            win32.click()
            time.sleep(0.2)
            setting_hwnd_list = win32.get_all_hwnds('SettingWnd', '设置')
            for s_hwnd in setting_hwnd_list:
                s_rect = win32.get_window_rect(s_hwnd)  # 窗口位置信息
                if 545 < s_rect[2] - s_rect[0] < 555 and 465 < s_rect[3] - s_rect[1] < 475:
                    win32.move2(s_hwnd, 322, 284, False)
                    win32.click()
                    time.sleep(0.3)
                    confirm_hwnd_list = win32.get_all_hwnds('ConfirmDialog', '微信')
                    for c_hwnd in confirm_hwnd_list:
                        win32.move2(c_hwnd, 225, 190, False)
                        win32.click()
        return True

    def get_account_list(self):
        """获取当前登入的账户列表"""  
        copy = self.all_account.copy()  
        for k, v in copy.items():
            if not win32.is_window(v):
                self.all_account.pop(k)
        exists = list(self.all_account.values()) 
        all_hwnds = win32.get_all_hwnds(self.body_class, self.title)
        all_hwnds = [h for h in all_hwnds if h not in exists]
        if all_hwnds:
            self.clear_screen_and_file(False)        
            for hwnd in all_hwnds:
                r = win32.get_window_rect(hwnd)  # 窗口位置信息
                win32.move2(hwnd, 30, r[3] - r[1] - 24)
                win32.click()
                time.sleep(0.2)
                win32.move2(hwnd, 120, r[3] - r[1] - 35, False)
                win32.click()
                time.sleep(0.2)
                setting_hwnd_list = win32.get_all_hwnds('SettingWnd', '设置')
                for s_hwnd in setting_hwnd_list:
                    pyperclip.copy('')
                    s_rect = win32.get_window_rect(s_hwnd)  # 窗口位置信息
                    if 545 < s_rect[2] - s_rect[0] < 555 and 465 < s_rect[3] - s_rect[1] < 475:
                        win32.move2(s_hwnd, 320, 235, False)
                        win32.click()
                        time.sleep(0.1)
                        win32.click()
                        time.sleep(0.2)
                        win32.ctrl_c()
                        time.sleep(0.2)
                        win32.key('ESC')  
                        account = pyperclip.paste()
                        account = account.replace('微信号：', '')
                        account = account.replace(' ','').replace(' ', '')  
                        if account:
                            pprint(account)
                            self.all_account.update({account: hwnd})                   
                # win32.move2(hwnd, 200, 10)
                # win32.click()
                # win32.move2(hwnd, 28, 35, active=False)
                # win32.click()
                # time.sleep(0.2)
                # file_dir = win32.screen_shot(hwnd, name='account-{}'.format(hwnd), x1=111, y1=90, x2=225, y2=120, temp_dir=self.temp_dir)              
                # account = self.check_exist(file_dir)
                # if not account:
                #     result = img.recognize(file_dir)
                #     pprint('-=======账号识别======')                   
                #     pprint(result)
                #     try:
                #         account_temp = result[0]['words']                   
                #         account = account_temp.replace('微信号:', '')
                #         account = account.replace(' ','').replace(' ', '')
                #         new_fir = os.path.join(self.account_dir, '{}.jpg'.format(account))
                #         if os.path.exists(new_fir):
                #             os.remove(new_fir)
                #         shutil.move(file_dir, new_fir)
                #     except Exception as e:
                #         pprint('-=======账号识别出错======')                   
                #         pprint(e.args[0])
                # if os.path.exists(file_dir):
                #     os.remove(file_dir)            
                
        return self.all_account

    def check_exist(self, file_dir):
        jpg_list = [x for x in os.listdir(self.account_dir)]
        result = []
        for jpg_name in jpg_list:
            account = os.path.splitext(jpg_name)[0]
            jpg_path = os.path.join(self.account_dir, jpg_name)
            r = img.compare(file_dir, jpg_path)
            if r > 0.9:
                result.append((account, r))
        if result:
            result.sort(key=lambda x: x[1])
            result = result[0][0]
            return result
        return False

    def send_msg(self, account, friend, content, msg_type='text'):
        """
        消息发送
        :param account: 微信账号
        :param friend:
        :param content:
        :param msg_type:
        :return:
        """
        hwnd = self.all_account.get(account)
        if hwnd and win32.is_window(hwnd):
            win32.move2(hwnd, 150, 10)
            win32.click()
            time.sleep(0.2)
            win32.move2(hwnd, 155, 40)
            win32.click()
            time.sleep(0.2)
            win32.paste_text(friend)
            time.sleep(1)
            if not self.check_friend(hwnd):
                return False
            win32.move2(hwnd, 180, 100)
            win32.click()
            time.sleep(0.5)

            rect = win32.get_window_rect(hwnd)  # 窗口位置信息
            if msg_type == 'text':
                win32.paste_text(content)
            elif msg_type == 'file':
                win32.move(rect[0] + 377, rect[3] - 119)
                time.sleep(0.2)
                win32.click()
                time.sleep(0.3)
                win32.paste_text(content)
                time.sleep(0.4)
                win32.key('o', ['ALT'])
            # send
            win32.move(rect[2] - 60, rect[3] - 21)
            win32.click()
            self.clear_screen_and_file()
            return True
        self.clear_screen_and_file(False)
        return False

    def clear_screen_and_file(self, clear_file=True):
        # 热键冲突
        for h in win32.get_all_hwnds('ConfirmDialog', '热键冲突'):
            time.sleep(0.5)
            win32.move2(h, 244, 188)
            win32.click()
        #  登出提示
        for h in win32.get_all_hwnds(self.tip_class, self.title):
            time.sleep(0.5)
            win32.move2(h, 180, 188)
            win32.click()
        # 打开文件窗口
        for h in win32.get_all_hwnds('#', '打开', fuzzy=True):
            time.sleep(0.5)
            win32.key('ESC')
        # 搜聊天记录窗口
        for h in win32.get_all_hwnds('FTSMsgSearchWnd', '微信'):
            time.sleep(0.5)
            win32.active_window(h)
            win32.key('ESC')
        if not clear_file:
            return True
        # 删除文件
        if self.send_count > 50:
            shutil.rmtree(self.temp_dir)
            # shutil.rmtree(self.pdf_dir)
            os.makedirs(self.temp_dir, 0o777)
            # os.makedirs(self.pdf_dir, 0o777)
            for path in [x for x in os.listdir(self.pdf_dir)]:
                if len(path) == 10 and path.count('-') == 2:
                    year, month, day = path.split('-')
                    today = date.today()
                    path_date = today.replace(year=int(year), month=int(month), day=int(day))
                    if (today - path_date).days >= 2:
                        shutil.rmtree(os.path.join(self.pdf_dir, path))
            self.send_count = 0
        else:
            self.send_count += 1

    def check_friend(self, hwnd):
        friend_img = win32.screen_shot(hwnd, name='friend-{}'.format(hwnd), x1=72, y1=105, x2=105, y2=137, temp_dir=self.temp_dir)
        r = img.compare(friend_img, self.search_icon)
        if r > 0.91:
            win32.move2(hwnd, 250, 37)
            win32.click()
            return False
        return True

wechat = WechatClient()


@task(name='微信登入')
def login():
    return wechat.login()

@task(wait=False, name='消息发送')
def send_msg(*args, **kwargs):
    return wechat.send_msg(*args, **kwargs)

@task(name='账户列表')
def get_account_list(*args, **kwargs):
    return wechat.get_account_list(*args, **kwargs)

def check_account(account):
    wechat.get_account_list()
    hwnd = wechat.all_account.get(account)
    return True if hwnd else False

def check_login(hwnd, wait=False):
    return wechat.check_login(hwnd, wait=wait)

if __name__ == "__main__":




    pass




