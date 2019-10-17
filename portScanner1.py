# -*- coding:utf-8 -*-
#original author:高海峰 
# QQ：543589796
# https://www.cnblogs.com/xuanhun/p/5950433.html?utm_source=tuicool&utm_medium=referral
#https://www.cnblogs.com/fanweibin/p/5053328.html
#
# python             3.7.3
# 
# 

from socket import *

# 定义端口扫描函数
# 对用于地址族，其中host是一个字符串，表示Internet域表示法中的主机名（如）或IPv4地址（如），而port是整数
def portScanner(host,port):
    try:
        # 参数一：表示地址簇
        # socket.AF_INET IPv4  （默认）
        # socket.AF_INET6 IPv6
        # socket.AF_UNIX        只能够用于单一的Unix系统进程间通信
        # 参数二：套接字类型
        # socket.SOCK_STREAM　　流式socket , for TCP （默认）
        # socket.SOCK_DGRAM　　 数据报式socket , for UDP
        # socket.SOCK_RAW       原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次，SOCK_RAW也可以处理特殊的IPv4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头。
        # socket.SOCK_RDM       是一种可靠的UDP形式，即保证交付数据报但不保证顺序。SOCK_RAM用来提供对原始协议的低级访问，在需要执行某些特殊操作时使用，如发送ICMP报文。SOCK_RAM通常仅限于高级用户或管理员运行的程序使用。
        # socket.SOCK_SEQPACKET 可靠的连续数据包服务
        s = socket(AF_INET,SOCK_STREAM,0)
        # 建立连接
        s.connect((host,port))
        print('[+] %s %d open' % (host,port))
        s.close()
    except:
        print('[-] %s %d close' % (host,port))

# 定义主函数
def main():
    # 这里对整个socket层设置超时时间
    setdefaulttimeout(1)
    # 遍历IP和port，调用端口扫描函数进行端口扫描
    for host in ip_list:
        for p in port:
            # 两个参数，分别是str和int
            portScanner(str(host),int(p))

if __name__ == '__main__':
    ip_list = ['172.16.21.64','172.16.21.69']
    port = ['80','22','3306']
    main()



