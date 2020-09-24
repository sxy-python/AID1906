from socket import *
import os,sys

#服务器地址
ADDR = ('127.0.0.1',1111)

#存储用户 {name,address}
user = {}

#登录
def do_login(s,name,addr):
    if name in user or '管理员' in name:
        s.sendto("该用户存在".encode(),addr)
        return

    # 加入用户
    msg = "\n欢迎 %s 进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name] = addr
    s.sendto(b'OK',addr)

#聊天
def do_chat(s,name,text):
    msg = "%s: %s" % (name,text)#说话的格式
    for i in user:
        #刨除其本人
        if i != name:
            s.sendto(msg.encode(),user[i])

#退出
def do_quit(s,name):
    msg = "%s 退出聊天室" % name
    for i in user:
        if i != name: #其他人发送
            s.sendto(msg.encode(),user[i])
        else: #本人
            s.sendto(b'EXIT',user[i])

    del user[name]#从字典中删除用户


def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        tmp = data.decode().split(' ')#拆分请求
        #根据不同的请求类型,执行不同的事情
        #L进入　C聊天　Q退出
        if tmp[0] == 'L':
            do_login(s,tmp[1],addr) #执行具体工作
        elif tmp[0] == 'C':
            text = ' '.join(tmp[2:])#元组拼字符串用join
            do_chat(s,tmp[1],text)
        elif tmp[0] == 'Q':
            do_quit(s,tmp[1])

#搭建网络
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid == 0:#子进程处理管理员消息

        while True:
            #子进程虽然有user,但是是空的,对user的操作,都是在父进程执行的
            msg = input("管理员消息:")
            msg = 'C ' + msg
            s.sendto(msg.encode(),ADDR)
    else:
        #请求处理函数
        do_request(s)


main()