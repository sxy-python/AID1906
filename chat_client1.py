from socket import *
import os,sys

#服务器地址
ADDR = ('127.0.0.1',1111)

#　发送消息
def send_msg(s,name):
    while True:
        try:
            text = input("发言:")#用终端
        except KeyboardInterrupt:
            text = 'quit'#防止服务器强行停止,而用户还没退出的情况,这里改为quit

        #strip()函数是去字符串左右两侧空格,怕输入手抖加空格
        if text.strip() == 'quit':
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = 'C %s %s' % (name,text)
        s.sendto(msg.encode(),ADDR)

#　接收消息
def recv_msg(s):
    while True:
        try:
            data,addr = s.recvfrom(4096)#用终端 和上面是两个进程(父子),但是使用的是同一个终端
        except KeyboardInterrupt:
            #从服务器收到EXIT退出
            if data.decode() == 'EXIT':
                sys.exit()
            print(data.decode())

#客户端启动函数
def main():
    s = socket(AF_INET,SOCK_DGRAM)

    #进入聊天室
    while True:
        name = input("请输入姓名:")
        # L是协议,服务器接收到了L,就知道了这是要进入聊天室
        # L后面加个空格,为了传到服务器的时候,方便解析
        msg = 'L ' + name
        s.sendto(msg.encode(),ADDR)

        #接收反馈
        data,addr = s.recvfrom(128)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    #已经进入聊天室,创建进程(父子分别负责收和发),正好有父子进程完美解决
    pid = os.fork()
    if pid < 0:#创建进程失败
        sys.exit("Error!")
    elif pid == 0:#子进程 　写成发消息(随便写收发都行)
        send_msg(s,name)  #子进程负责消息发送
    else:#父进程 写成收消息
        recv_msg(s) #　父进程负责消息接收





main()

