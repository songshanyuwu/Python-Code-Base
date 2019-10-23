# -*- coding:utf-8 -*-
#original author: 
# #该片段来自于http://outofmemory.cn
# 
#
# python             3.7.3
# 
# 

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
探测网络主机存活。
'''

import os
import struct
import array
import time
import socket
import IPy
import threading

class SendPingThr(threading.Thread):
    '''
    发送ICMP请求报文的线程。

    参数：
        ipPool      -- 可迭代的IP地址池
        icmpPacket  -- 构造的icmp报文
        icmpSocket  -- icmp套字接
        timeout     -- 设置发送超时
    '''
    def __init__(self, ipPool, icmpPacket, icmpSocket, timeout=3):
        threading.Thread.__init__(self)
        self.Sock = icmpSocket
        self.ipPool = ipPool
        self.packet = icmpPacket
        self.timeout = timeout
        self.Sock.settimeout( timeout + 3 )

    def run(self):
        time.sleep(0.01)  #等待接收线程启动
        for ip in self.ipPool:
            try:
                self.Sock.sendto(self.packet, (ip, 0))
            except socket.timeout:
                break
        time.sleep(self.timeout)

class Nscan:
    '''
    参数：
        timeout    -- Socket超时，默认3秒
        IPv6       -- 是否是IPv6，默认为False
    '''
    def __init__(self, timeout=3, IPv6=False):
        self.timeout = timeout
        self.IPv6 = IPv6

        self.__data = struct.pack('d', time.time())   #用于ICMP报文的负荷字节（8bit）
        self.__id = os.getpid()   #构造ICMP报文的ID字段，无实际意义

    @property   #属性装饰器
    def __icmpSocket(self):
        '''创建ICMP Socket'''
        # if os.name == 'nt':
        #     #no root on windows
        if not self.IPv6:
            Sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        else:
            Sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.getprotobyname("ipv6-icmp"))
        return Sock

    def __inCksum(self, packet):
        '''ICMP 报文效验和计算方法'''
        if len(packet) & 1:
            packet = packet + '\\0'
        words = array.array('h', packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)

        return (~sum) & 0xffff

    @property
    def __icmpPacket(self):
        '''构造 ICMP 报文'''
        if not self.IPv6:
            header = struct.pack('bbHHh', 8, 0, 0, self.__id, 0) # TYPE、CODE、CHKSUM、ID、SEQ
        else:
            header = struct.pack('BbHHh', 128, 0, 0, self.__id, 0)

        packet = header + self.__data     # packet without checksum
        chkSum = self.__inCksum(packet) # make checksum

        if not self.IPv6:
            header = struct.pack('bbHHh', 8, 0, chkSum, self.__id, 0)
        else:
            header = struct.pack('BbHHh', 128, 0, chkSum, self.__id, 0)

        return header + self.__data   # packet *with* checksum

    def isUnIP(self, IP):
        '''判断IP是否是一个合法的单播地址'''
        IP = [int(x) for x in IP.split('.') if x.isdigit()]
        if len(IP) == 4:
            if (0 < IP[0] < 223 and IP[0] != 127 and IP[1] < 256 and IP[2] < 256 and 0 < IP[3] < 255):
                return True
        return False

    def makeIpPool(self, startIP, lastIP):
        '''生产 IP 地址池'''
        IPver = 6 if self.IPv6 else 4
        intIP = lambda ip: IPy.IP(ip).int()
        ipPool = {IPy.intToIp(ip, IPver) for ip in range(intIP(startIP), intIP(lastIP)+1)}

        return {ip for ip in ipPool if self.isUnIP(ip)}

    def mPing(self, ipPool):
        '''利用ICMP报文探测网络主机存活

        参数：
            ipPool  -- 可迭代的IP地址池
        '''
        Sock = self.__icmpSocket
        Sock.settimeout(self.timeout)
        packet = self.__icmpPacket
        recvFroms = set()   #接收线程的来源IP地址容器

        sendThr = SendPingThr(ipPool, packet, Sock, self.timeout)
        sendThr.start()

        while True:
            try:
                recvFroms.add(Sock.recvfrom(1024)[1][0])
            except Exception:
                pass
            finally:
                if not sendThr.isAlive():
                    break
        return recvFroms & ipPool

if __name__=='__main__':
    start_time = time.time()
    s = Nscan()
    # 构造地址池，输入指定开始IP和结束IP
    ipPool = s.makeIpPool('172.16.2.1', '172.16.2.254')
    avtive_ip = s.mPing(ipPool)
    print( set(avtive_ip) )
    print('存活IP地址数量：',len(avtive_ip))
    end_time = time.time()
    print('耗时：',(end_time-start_time))
