#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:songshanyuwu
# datetime:2019/12/31 22:16
# software: V1.0
# 将log日志的typeName字段进行筛选，统计各自发生的次数

import sys
import os
import json
import xlwt
import time

# 用于简单程序运行时间计算
begin_time = time.time()

# 在内存中创建表格，并建立sheet，定义标题
f1 = xlwt.Workbook()
sheet1 = f1.add_sheet('XXX_typeName',cell_overwrite_ok=True)   #第二个参数用于确认同一个cell单元是否可以重设值
sheet1.write(0,0,'typeName')
sheet1.write(0,1,'count')

# 打开指定文件读取所有行，以后根据需要改为同目录下文件依次打来执行
with open(os.path.dirname(__file__) + '/weblog-2019121802.log', 'r', encoding='utf-8') as f:   
    content = f.readlines()
    f.close()

# 定义用于统计的字典
typeName = {}

# 对文件内容逐行进行判断和处理
for line in content:
    # 处理空行和空格组成的行
    if (line in ['\n','\r\n']) or (line.strip() == ""):
        pass
    else:
        # 格式化json，读取typeName字段。存在字典中则值＋1，不存在则新增且值=1
        json_str = json.loads(str(line))
        typeNameStr = json_str["typeName"]
        if typeNameStr not in typeName.keys():
            typeName.update([(typeNameStr,1)])
        else:
            typeNameNum = typeName[typeNameStr]+1
            typeName.update({typeNameStr:typeNameNum})

# 测试用便利字典内容
# for key, value in typeName.items():
#     print(str(value) + ' ' + key)

# 直接将字典输出，结果是乱序的，遂弃之。
# m = 0
# for key, value in typeName.items():
#     sheet1.write(m,0,key)
#     sheet1.write(m,1,value)
#     m+=1


# 对字典按照键的大小进行排序后，再写入表格
# by_key =  sorted(typeName.items(),key = lambda item:item[0])
# by_value1 = sorted(typeName.items(),key = lambda item:item[1])
by_value2 = sorted(typeName.items(),key = lambda item:item[1],reverse = True)
# print by_key   #结果为[(1, 3), (2, 2), (3, 1)]，即按照键名排列，从小到大
# print by_value1 #结果为[(3, 1), (2, 2), (1, 3)]，即按照键值排列，从小到大
# 将排序后的列表进行遍历，遍历的是元祖，将两个值写入表格
m = 1
for listValue in by_value2:
    sheet1.write(m,0,listValue[0])
    sheet1.write(m,1,listValue[1])
    m+=1

# 表格存储，生成结果
f1.save(os.path.dirname(__file__) + '/' +'XXX_typeName.xls')

# 用于简单程序运行时间计算
end_time = time.time()
run_time = end_time-begin_time
print ('该程序运行时间：',run_time) #该循环程序运行时间： 1.4201874732









