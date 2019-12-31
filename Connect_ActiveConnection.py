#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:songshanyuwu
# datetime:2019/12/31 23:33
# software: V0.9
# 将log日志的typeName字段进行筛选“连接”，然后从“主动连接”事件中再进行筛选

import sys
import os
import json
import xlwt
import time

# 用于简单程序运行时间计算
begin_time = time.time()


notInList = [':44567','System','sinopec','114.114.114.114','www.w3.org','notepad-plus-plus.org',
             'usage.projectcalico.org','python',"172.",'ntp.org','mariadb.org','google.com','taobao.org',
             'mozilla.org','eclipse.exe','360se.exe','repo1.maven.org','mirrors.fedoraproject.org']

inList = ['38.102.150.27',':445','.xmrig.com','4i7i.com','santa.inseription.com','xmr.','.onion.ws',
          'org','coco.miniast.com','lpp.awcna.com','arthur520.cn','wakuang','xcn1.yiluzhuanqian.com',
          '.f2pool.com','xmr.crypto-pool.fr','jw-js1.ppxxmr.com','fr.minexmr.com','pool.minexmr.com',
          '.ru','jidan5201314']

# 在内存中创建表格，并建立sheet，定义标题
f1 = xlwt.Workbook()
sheet1 = f1.add_sheet('G01_ActiveConnection',cell_overwrite_ok=True)   #第二个参数用于确认同一个cell单元是否可以重设值
sheet1.write(0,0,'company')
sheet1.write(0,1,'webIp')
sheet1.write(0,2,'process')
sheet1.write(0,3,'IP')
sheet1.write(0,4,'port')
sheet1.write(0,5,'count')
sheet1.write(0,6,'other')

# 打开指定文件读取所有行，以后根据需要改为同目录下文件依次打来执行
with open(os.path.dirname(__file__) + '/weblog-2019121802.log', 'r', encoding='utf-8') as f:   
    content = f.readlines()
    f.close()

# 对文件内容逐行进行判断和处理
m = 1
for i in content:
    if "主动连接" in i:
        json_str = json.loads(str(i))
        # company = json_str["hKList"]["company"]
        webIp = json_str['webIp']
        js1 = json_str["action"]["text"]

        if ':44567' not in js1 and 'System' not in js1 and 'sinopec' not in js1 and '114.114.114.114' not in js1 and 'www.w3.org' not in js1 and 'notepad-plus-plus.org' not in js1 and 'usage.projectcalico.org' not in js1 and 'python' not in js1 and "172." not in js1 and 'ntp.org' not in js1 and 'mariadb.org' not in js1 and 'google.com' not in js1 and 'taobao.org' not in js1 and 'mozilla.org' not in js1 and 'eclipse.exe' not in js1 and '360se.exe' not in js1 and 'repo1.maven.org' not in js1 and 'mirrors.fedoraproject.org' not in js1:
        #     if '38.102.150.27' in js1 or ':445' in js1 or '.xmrig.com' in js1 or '4i7i.com' in js1 or 'santa.inseription.com'  in js1 or 'xmr.' in js1 or '.onion.ws' in js1 or 'org' in js1 or 'coco.miniast.com' in js1 or 'lpp.awcna.com' in js1 or 'arthur520.cn' in js1 or 'wakuang' in js1 or 'xcn1.yiluzhuanqian.com' in js1 or '.f2pool.com' in js1 or 'xmr.crypto-pool.fr' in js1 or 'jw-js1.ppxxmr.com' in js1 or 'fr.minexmr.com' in js1 or 'pool.minexmr.com' in js1 or '.ru' in js1 or 'jidan5201314' in js1:
            for bb in inList:
                if js1.count(bb):
                    # print(webIp,"---",js1)
                    # sheet1.write(m,0,company)
                    sheet1.write(m,1,webIp)
                    a,process,ipport,d,e = js1.split(' ',4)
                    ip,port = ipport.split(':',1)
                    # print(a+'//'+process+'//'+c+'//'+d+'//'+e)
                    sheet1.write(m,2,process) # process
                    sheet1.write(m,3,ip) # ip
                    sheet1.write(m,4,port) # port
                    sheet1.write(m,6,d) # other
                    # 数据没有汇总透视，以目前样本分析不重复的 占所有的25% 
                    m = m+1

# 表格存储，生成结果
f1.save(os.path.dirname(__file__) + '/' +'g011.xls')

# 用于简单程序运行时间计算
end_time = time.time()
run_time = end_time-begin_time
print ('该程序运行时间：',run_time) #该循环程序运行时间： 1.4201874732
