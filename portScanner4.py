# -*- coding:utf-8 -*-
#original author:高海峰 
# QQ：543589796
# https://www.cnblogs.com/xuanhun/p/5950433.html?utm_source=tuicool&utm_medium=referral
# https://www.cnblogs.com/fanweibin/p/5053328.
# https://www.cnblogs.com/kxsph/p/9234156.html
# 同时还参考wolf@future-sec的F-NAScan
#
# python             3.7.3
# socket            
# argparse                
# 
# python3内置两个thread模块：
#    1、_thread模块
#    2、threading模块  ← 推荐使用threading模块
# 
# 获取参数IP和port，然后对给定的参数进行端口扫描


import socket
import threading
import getopt
import sys,os,time


lock = threading.Lock()
threads = []
openNum = 0


def portScanner(host,port):
    # 记录单个IP开启端口的数量
    global openNum
    # 设置超时时间0.1秒
    # 扫描一个IP的65535个端口大约需要152秒左右，与开启端口数量有关。
    # 扫描一个C段所有IP的1个端口大约需要26秒左右
    # 扫描一个C段所有端口大约10小时，┭┮﹏┭┮好low啊
    timeout = 0.1
    try:
        time_str = time.strftime('%X', time.localtime(time.time()))
        # 超时可以在这设置
        # #socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 超时也可以在这设置
        s.settimeout(timeout)
        s.connect((host,port))
        lock.acquire()  # 获取锁
        openNum+=1
        print('[-{:^8}-] {:>5} {:>6} open'.format(time_str,host,port))
        lock.release()  # 锁释放
        s.close()
    except:
        pass


# 扫描指定端口 如： 22,80,139,445,3306,3389
def ThreadNum(host_list,port_list):
    for host in host_list:
        #print('Scanning the host:%s......' % (host))
        if isinstance(port_list,str):
            port = port_list
            t = threading.Thread(target=portScanner,args=(host,int(port)))
            threads.append(t)
            t.start()
        else:
            for p in port_list:
                port = p
                # print(host,int(port))
                t = threading.Thread(target=portScanner,args=(host,int(port)))
                threads.append(t)
                t.start()
        # 等待至线程中止。
        for t in threads:
            # 这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
            t.join()
            # 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。
            #print(threading.activeCount())
        # print('[***] The host:%s scan is complete!' % (host))
        # print('[***] A total of %d open port ' % (openNum))
        # print()


# 从传入的参数解析生成ip_list列表
def get_ip_list(ipstr):
    ip_list = []
    # 如果格式是172.16.0.1-100
    if '-' in ipstr:
        ip_range = ipstr.split('-')
        ip_start = int(ip_range[0].split('.')[3])
        ip_end = int(ip_range[1])
        ip_count = ip_end - ip_start
        if ip_count >= 0 and ip_count <= 65536:
            for ip_num in range(ip_start,(ip_end+1)):
                ip = ip_range[0].split('.')[0] + '.' + ip_range[0].split('.')[1] + '.' + ip_range[0].split('.')[2] + '.' + str(ip_num)
                ip_list.append(ip)
        else:
            print( '-h wrong format')
    # 如果是从ini文件中获取
    elif '.ini' in ipstr:
        ip_config = open('ip.ini','r')
        for ip in ip_config:
            ip_list.extend(get_ip_list(ip.strip()))
        ip_config.close()
    # 如果IP地址的格式是10.0或者10.10.0或者10.10.10.0的不同处理方式
    else:
        ip_split=ipstr.split('.')
        net = len(ip_split)
        if net == 2:
            for b in range(1,255):
                for c in range(1,255):
                    ip = "%s.%s.%d.%d"%(ip_split[0],ip_split[1],b,c)
                    ip_list.append(ip)
        elif net == 3:
            for c in range(1,255):
                ip = "%s.%s.%s.%d"%(ip_split[0],ip_split[1],ip_split[2],c)
                ip_list.append(ip)
        elif net ==4:
            ip_list.append(ipstr)
        else:
            print( "-h wrong format")
    return ip_list


# 从传入的参数解析生成port_list列表
def get_port_list(portstr):
    port_list = []
    if '.ini' in portstr:
        port_config = open('port.ini','r')
        for port in port_config:
            port_list.append(port.strip())
        port_config.close()
    elif '-' in portstr:
        port_range = portstr.split('-')
        port_start = int(port_range[0])
        port_end = int(port_range[1])
        port_count = port_end - port_start
        if 0 <= port_count <= 65536:
            for port_num in range(port_start,(port_end+1)):
                port_list.append(port_num)
    elif ',' in portstr:
        port_list = portstr.split(',')
    elif len(portstr) != 0:
        port_list = portstr
    else:
        port_list = [21,22,23,25,53,80,110,139,143,389,443,445,465,873,993,995,1080,1723,1433,1521,3306,3389,3690,5432,5800,5900,6379,7001,8000,8001,8080,8081,8888,9200,9300,9080,9999,11211,27017]
    return port_list


def main():
    msg = '''
Scanning a network asset information script,author:songshanyuwu.
Usage: python portScanner4.py -h 192.168.1 [-p 21,80,3306]
-h ip： 192.168.1.1 | 192.168.1 | 172.16 | ip.ini | 192.168.1.1-100
-p port: 1-65535 | 22,80,443,3389 | port.ini | Null
    '''
    err = ''
    ipstr = ''
    portstr = ''

    # 如果报错则打印提示信息
    if len(sys.argv) < 2:
        print(msg)
    try:
        options,args = getopt.getopt(sys.argv[1:],"h:p:")
        for opt,arg in options:
            if opt == '-h':
                ipstr = arg
            elif opt == '-p':
                portstr = arg
        # 测试用数据
        # ipstr = '172.16.21.60-99'
        # portstr = '22,80,443,3389'
        host_list = get_ip_list(ipstr)
        port_list = get_port_list(portstr)
        # 开始扫描端口
        ThreadNum(host_list,port_list)
    except Exception as err:
        #print(err)
        print( msg)


if __name__ == '__main__':
    main()
