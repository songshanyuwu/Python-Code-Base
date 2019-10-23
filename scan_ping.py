# -*- coding:utf-8 -*-
# original author: 郑瑞国
# 
# 
# python             3.7.3
# 
'''
Python 局域网扫描存活主机开放端口 by 郑瑞国
1、ping指定IP判断主机是否存活
2、ping所有IP获取所有存活主机
#注: 若在Linux系统下 ping -n 改为 ping -c 
     若在windows系统下 ping -n 不变
'''

import socket
import os
import threading
import time 

#  获取本机的IP地址
#print(socket.gethostbyname(socket.gethostname()))

IPList = [] 
def ping_ip(ip):                                          #1、ping指定IP判断主机是否存活
    #print(ip)
    output = os.popen('ping -n 1 %s'%ip).readlines()      #注：若在Linux系统下-n 改为 -c
    for w in output:
        if str(w).upper().find('TTL')>=0:
            IPList.append(ip)
            print(ip)
 
def ping_net(ip):                                         #2、ping所有IP获取所有存活主机
    pre_ip = (ip.split('.')[:-1])
    #print(pre_ip)
    for i in range(1,256):
        add = ('.'.join(pre_ip)+'.'+str(i))
        threading._start_new_thread(ping_ip,(add,))
        time.sleep(0.1)

 
if __name__ == '__main__':
    start_time = time.time()
    #print(socket.gethostbyname(socket.gethostname()))
    #ping_net(socket.gethostbyname(socket.gethostname()))
    ping_net('192.168.101.59')
    print(len(IPList))
    end_time = time.time()
    print('耗时：',(end_time-start_time))
