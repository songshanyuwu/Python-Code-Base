# -*- coding:utf-8 -*-
#original author:高海峰 
# QQ：543589796
# https://www.cnblogs.com/xuanhun/p/5950433.html?utm_source=tuicool&utm_medium=referral
# https://www.cnblogs.com/fanweibin/p/5053328.html
# 同时还参考wolf@future-sec的F-NAScan
#
# python             3.7.3
# socket            
# argparse                
# 
# python3内置两个thread模块：
#    1、_thread模块
#    2、threading模块  ← 推荐使用threading模块


from socket import *
import threading
import argparse

lock = threading.Lock()
openNum = 0
threads = []

def portScanner(host,port):
    global openNum
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        lock.acquire()
        openNum+=1
        print('[+] %s %d open' %(host,port))
        lock.release()
        s.close()
    except:
        pass


# 扫描端口段 如： 1-65535
def ThreadNum1(hostList, start, end):
    setdefaulttimeout(1)
    for host in hostList:
        print('Scanning the host:%s......' % (host))
        for port in range(start, end):
            t = threading.Thread(target=portScanner,args=(host,int(port)))
            threads.append(t)
            t.start()     

        for t in threads:
            t.join()

        print('[***] The host:%s scan is complete!' % (host))
        print('[***] A total of %d open port ' % (openNum))
        print()


# 扫描指定端口 如： 22,80,139,445,3306,3389
def ThreadNum2(hostList,port_list):
    setdefaulttimeout(1)
    for host in hostList:
        print('Scanning the host:%s......' % (host))
        for port in port_list:
            t = threading.Thread(target=portScanner,args=(host,int(port)))
            threads.append(t)
            t.start()     

        for t in threads:
            t.join()

        print('[***] The host:%s scan is complete!' % (host))
        print('[***] A total of %d open port ' % (openNum))
        print()



def main():

    # 创建一个解析对象; description 参数可以用于插入描述脚本用途的信息，可以为空
    parser = argparse.ArgumentParser(description='Port scanner!.')

    # 向该对象中添加你要关注的命令行参数和选项
    #                  可以同时指定短参数和长参数                                  type设置默认参数类型
    parser.add_argument('-H', '--hosts', dest='hosts', help = '请输入主机名或IP', type=str)
    
    parser.add_argument('-P', '--ports', dest='ports', help = '请输入端口段或指定端口： 1-65535 或 22，80，443', type=str)

    # 通过choices来限定某个值的取值范围
    #parser.add_argument("-V", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")
    
    # 定义了一个互斥组， 根据需简要设定
    # 通过action来设置互斥参数，-q 和 -v 不出现，或仅出现一个都可以，同时出现就会报错。
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-q", action="store_true")
    #group.add_argument("-v",  action="store_true")
    
    # 进行解析
    args = parser.parse_args()

    # 获取收集的参数
    hostList = args.hosts.split(',')
    # 对端口进行判断分析:
    # 如果是1-65535，则执行ThreadNum1()
    # 如果是22 或者 22，80， 或者不填写，则执行ThreadNum2()
    if args.ports :
        port_list = []
        start = 1
        end = 65535
        if '-' in args.ports:
            start, end = args.ports.split('-')
            ThreadNum1(hostList, int(start), int(end))
        elif ',' in args.ports:
            port_list = args.ports.split(',')
            ThreadNum2(hostList, port_list)
        elif args.ports.isdigit() and 1 <= int(args.ports) <= 65535:
            port_list = args.ports
            ThreadNum2(hostList, port_list)
        else:
            print('请检查-P参数的格式！')
            exit
    else:
        port_list = [21,22,23,25,53,80,110,139,143,389,443,445,465,873,993,995,1080,1723,1433,1521,3306,3389,3690,5432,5800,5900,6379,7001,8000,8001,8080,8081,8888,9200,9300,9080,9999,11211,27017]
        ThreadNum2(hostList, port_list)


if __name__ == '__main__':
    main()
