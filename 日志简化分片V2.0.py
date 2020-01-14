#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:songshanyuwu
# datetime:2019/12/31 23:33
# software: V0.9
# 将log日志的typeName、IP、innerIP、action.text字段筛选出来
# 注意38-39行用来指定事件类型

import sys
import os
import json
import xlwt
import time

# 用于简单程序运行时间计算
begin_time = time.time()
print(os.getcwd())
# 打开指定文件读取所有行，以后根据需要改为同目录下文件依次打来执行
#with open(os.path.dirname(__file__) + '/2020-01-01.log', 'r', encoding='utf-8') as f:   
with open(os.getcwd() + '/2020-01-01.log', 'r', encoding='utf-8') as f:   
    content = f.readlines()
    f.close()

# 定义循环变量用于设定行数m 和txt编号num
m = 1
num = 1
#txtName = os.path.dirname(__file__) + '/' +'g01-日志简化-' + str(num) + '.txt'
txtName = os.getcwd() + '/' +'g01-日志简化-' + str(num) + '.txt'
f = open(txtName,'w', encoding='utf-8')

# 对文件内容逐行进行判断和处理
for line in content:
    # 处理空行和空格组成的行
    if (line in ['\n','\r\n']) or (line.strip() == ""):
        pass
    else:
        # 格式化json
        json_str = json.loads(str(line))
        typeName = json_str['typeName']

        # 下面的用来筛选typeName的类型
        #if typeName != "服务器疑似被入侵":
        #    continue

        innerIp = json_str['innerIp']
        actionText = json_str["action"]["text"]
        # 因为IP字段不一定存在，需要判断
        try:
            IP = json_str['Ip']
        except KeyError:
            IP = ''

        # 各字段写入表格
        new_context = typeName + ' , ' + IP + ' , ' + innerIp + ' , ' + actionText
        f.write(new_context)    
        f.write('\n') 
        # 需要判断是否超过表格的存储数量
        m += 1
        if m > 50000:
            m = 0
            # 生成TXT分片的结果
            f.close()
            num += 1
            # 重新再开新的文件用于存储内容
            #txtName = os.path.dirname(__file__) + '/' +'g01-日志简化-' + str(num) + '.txt'
            txtName = os.getcwd() + '/' +'g01-日志简化-' + str(num) + '.txt'
            f = open(txtName,'w', encoding='utf-8')


# 表格存储，生成结果
f.close()

# 用于简单程序运行时间计算
end_time = time.time()
run_time = end_time-begin_time
print ('该程序运行时间：',run_time) #该循环程序运行时间： 1.4201874732
