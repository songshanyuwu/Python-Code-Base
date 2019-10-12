# -*- coding:utf-8 -*-
#original author: injetlee
# https://github.com/injetlee/Python/blob/master/CpuToInfluxdb.py

# python             3.7.3
# psutil             5.6.3
#
# 实时监控系统的内存占用率和CPU占用率,去除了influxdb库以及相关代码

import psutil
import os
import time
#from influxdb import InfluxDBClient

#获取当前运行的pid
p1=psutil.Process(os.getpid()) 

while True:
    a = psutil.virtual_memory().percent  #内存占用率
    b = psutil.cpu_percent(interval=1.0) #cpu占用率
    print("\r","内存占用率:{:<8}     CPU占用率:{:<8}".format(b,a),end="",flush=True)
    time.sleep(2)
