# -*- coding: UTF-8 -*-

import time
from _winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
import ConfigParser

config = ConfigParser.ConfigParser()

def now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def log_width():
    return 60


def start_line():
    return '=' * log_width()


def end_line():
    return '-' * log_width()

def is_float(str):
    try:
        float(str)
        return True
    except Exception, e:
        return False

def my_documents_path():
    key = OpenKey(HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return QueryValueEx(key, 'Personal')[0]


def show_message(msg, title, icon):
    dlg = wx.MessageDialog(None, msg, title, wx.OK | icon)
    dlg.ShowModal()
    dlg.Destroy()

def info_message(msg):
    show_message(msg, 'Information', wx.ICON_INFORMATION)

def warning_message(msg):
    show_message(msg, 'Warning', wx.ICON_WARNING)

#获取配置文件的ip
def getIP():
    config.read('config.ini')
    return config.get("IP","ip")

#将ip写入配置文件
def setIP(ip):
    config.read('config.ini')
    oldIP = config.get("IP", "ip")
    if oldIP != ip:
        config.set("IP","ip",ip)
        config.write(open('config.ini', "r+"))
