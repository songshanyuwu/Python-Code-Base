# -*- coding:utf-8 -*-
# original author: songshanyuwu
# python             3.7.3
# 查询记事本逐行查看每行所有IP地址，取最后一个IP地址。

import re
from openpyxl import Workbook
import csv
import os


fileName=r'C:\Users\songz\Desktop\新建文件夹\茂名分公司sql注入日志.txt'
print(fileName)

txtName = r'C:\Users\songz\Desktop\新建文件夹\茂名分公司sql注入日志--R.txt'
txtfile=open(txtName, "a+")





i = 1
tmplist = []
with open(fileName,newline='',encoding='UTF-8') as csvfile:
# with open(fileName,newline='', encoding = 'GB2312') as csvfile:
    rows=csv.reader(csvfile)
    # print(rows)

    for row in rows:
        # print(row)
        # 过滤掉首行标题，选择指定‘端口异常’的事件类型
        if i == 1 :
            pass
        else:
            # print(str(row))
            result = re.findall(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", str(row))
            # result = re.findall(r"\d+.\d+.\d+.\d+", str(row))
            # print(result[-1])
            if result[-1] in tmplist:
                pass
            else:
                tmplist.append(result[-1])

            
        i += 1


for val in tmplist:
    txtfile.write(val + '\n')

txtfile.close()




