# -*- coding:utf-8 -*-
# original author: songshanyuwu
# python             3.7.3


import re
from openpyxl import Workbook
import csv
import os
import pandas as pd
# 进行具体的sum,count等计算时候要用到的
import numpy as np


# 输入需要处理的文件
src_fileName=r'C:/Users/songz/Desktop/新建文件夹/query_result.csv'
# print(src_fileName)

# 要创建的目标文件
dest_filename = src_fileName.split('.')[0] + '-端口异常.csv'
dest_filename2 = src_fileName.split('.')[0] + '-类型统计.csv'
# print(dest_filename)

#测试数据。
df = pd.DataFrame(data = [],index = [],columns = ['ip','process','port'])
# print(df.head())
# print('ok')

# 将文件逐行读取，通过正则获取到ip ,process ,port；将其写入到pandas的DataFrame中
i = 0
with open(src_fileName,newline='',encoding='UTF-8') as csvfile:
# with open(src_fileName,newline='', encoding = 'GB2312') as csvfile:
    rows=csv.reader(csvfile)
    # print(rows)
    for row in rows:
        # print(row)
        # 过滤掉首行标题，选择指定‘端口异常’的事件类型
        if row[0] == 'typeName' or row[0] != '端口异常':
            pass
        else:
            result = re.findall(r"进程(?P<value>[A-Za-z0-9\.]+)", row[1])
            result2 = re.findall(r"监听(?P<value>[A-Za-z0-9\.]+)端口", row[1])
            # print(result)
            # print(result2)
            ip = row[2]

            try:
                for process in result:
                    for port in result2:
                        # print(ip ,process ,port)
                        df.loc[i] = [ip ,process ,port]
            except:
                process = ''
                for port in result2:
                        # print(ip ,process ,port)
                        df.loc[i] = [ip ,process ,port] 
            i += 1

# 分组统计
gp=df.groupby(by=['ip','process','port'])
# 如果想统计更多列，只要在groupby()中的by参数添加就可以，例如统计3列
# gp=df.groupby(by=['A','B','C'])
# gp.size()得到的是可以mulitiindex Series
gp.size()

# 转化成DataFrame的结构
newdf=gp.size()
res = newdf.reset_index(name='counts')
# print(newdf.reset_index(name='counts'))

# by 指定列 ascending （顺序还是降序）
res.sort_values(by="counts" , ascending=True) 

# 把结果写进结果文件
res.to_csv(dest_filename, encoding="utf_8_sig",index=False)
print(dest_filename + '    OK')


# ###############################


# 这里绝对路径一定要用/,windows下也是如此,不加参数默认csv文件首行为标题行
df=pd.read_csv(src_fileName)

# 分组统计
gp=df.groupby(by=['typeName','innerIp'])
# gp.size()得到的是可以mulitiindex Series
gp.size()

# 转化成DataFrame的结构
newdf=gp.size()
res = newdf.reset_index(name='counts')
# print(newdf.reset_index(name='counts'))

# # by 指定列 ascending （顺序还是降序）
# res.sort_values(by="counts" , ascending=True) 

# 指定多列排序(注意：对Worthy列升序，再对Price列降序)，ascending不指定的话，默认是True升序
# res.sort_values(by=["Worthy","Price"],inplace=True,ascending=[True,False])

# 把结果写进结果文件
res.to_csv(dest_filename2, encoding="utf_8_sig",index=False)

print(dest_filename2 + '     OK')




