# -*- coding:utf-8 -*-
#original author:高海峰 
# QQ：543589796
# https://www.cnblogs.com/xuanhun/p/5950433.html?utm_source=tuicool&utm_medium=referral
#https://www.cnblogs.com/fanweibin/p/5053328.html
#
# python             3.7.3
# socket            
# threading          
#
#


from socket import *
import threading

# 设置互斥所
lock = threading.Lock()
openNum = 0
threads = []

# 定义端口扫描函数
def portScanner(host,port):
    # 
    global openNum
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        # 获取底层锁
        lock.acquire()
        openNum+=1
        print('[+] %s %d open' % (host,port))
        # 释放底层锁
        lock.release()
        s.close()
    except:
        pass

def main(ip_list,ports):
    setdefaulttimeout(1)
    # Thread ： 表示一个执行线程的对象　,表示在单独的控制线程中运行的活动。
    # 主要方法：
    # threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
    # target是将被run()方法调用的可调用对象。默认为None，表示不调用任何东西。
    # name是线程的名字。默认情况下，以“Thread-N”的形式构造一个唯一的名字，N是一个小的十进制整数。
    # args是给调用目标的参数元组。默认为()。
    # kwargs是给调用目标的关键字参数的一个字典。默认为{}
    # daemon表示是否为守护线程
    # start()               //开始执行线程　　
    # run()                 //定义线程功能
    # join(timeout=None)　　//直至启动的线程之前一直挂起，除非给出timeout时间，否则一直阻塞
    # gerName()             //返回线程名
    # 属性：
    # name　　  //线程名
    # ident　　 //线程标识符
    # daemon　　//是否为守护线程
    
    # for p in range(1,1024):
    #     # 设置线程，调用函数portScanner，并传入参数
    #     t = threading.Thread(target=portScanner,args=('172.16.21.64',p))
    #     # 将t添加到列表中
    #     threads.append(t)
    #     # 开始执行线程
    #     t.start()     

    for ips in ip_list:
        for port in ports:
            # 设置线程，调用函数portScanner，并传入参数
            t = threading.Thread(target=portScanner,args=(str(ips),int(port)))
            # 将t添加到列表中
            threads.append(t)
            # 开始执行线程
            t.start()     

    for t in threads:
        # 直至启动的线程之前一直挂起，除非给出timeout时间，否则一直阻塞。
        # 这里在本函数首行已经设置timeout时间了
        t.join()

    print('[**] The scan is complete!')
    print('[**] A total of %d open port ' % (openNum))

if __name__ == '__main__':
    ip_list = ['172.16.21.64','172.16.21.69']
    ports = ['22','80','110','139','445','3306']
    main(ip_list,ports)
