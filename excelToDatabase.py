# -*- coding:utf-8 -*-
# original author: injetlee
# https://github.com/injetlee/Python
#
# python             3.7.3
# 
#excelToDatabase.py
# 把Excel文件的数据写入到数据库中

from openpyxl import load_workbook
import pymysql

# 配置数据库连接的信息
config = {
    'host': '127.0.0.1',
    'port':3306,
    'user': 'root',
    'password': 'root',
    'charset': 'utf8mb4',
    #'cursorclass': pymysql.cursors.DictCursor

}
# 建立数据库连接
conn = pymysql.connect(**config)
conn.autocommit(1)
cursor = conn.cursor()

# 设置数据库名称，如果不存在则创建；然后调用该数据库
database_name = 'masscan'
cursor.execute('create database if not exists %s' % database_name)
conn.select_db(database_name)
# 设置表名称，如果不存在则创建
table_name = 'info1'
sql1 = "CREATE TABLE if not exists " + table_name + "(id BIGINT(20), ip VARCHAR(15), port_id MEDIUMINT(8), scanned_ts TIMESTAMP(0), protocol enum('tcp', 'udp'), state VARCHAR(10), reason VARCHAR(255), reason_ttl INT(10), service VARCHAR(100), banner text, title text)"
cursor.execute(sql1)

# 加载Excel表文件
wb2 = load_workbook('masscan_data.xlsx')
# 获取sheet的名称
ws=wb2.get_sheet_names()

# 先遍历每一行，在从每一行中遍历单元格
for row in wb2:
    for cell in row:
        value1=(cell[0].value,cell[1].value,cell[2].value,cell[3].value,cell[4].value,cell[5].value,cell[6].value,cell[7].value,cell[8].value,cell[9].value,cell[10].value)
        print(value1)
        # 判断是否是首列，首列则跳过，进入下面的循环
        if cell[0].value == 'id':
            continue
        else:
            # 将读取的数据，通过语句写入到数据库中
            #                     ↓ 这里我直接指定了
            sql2 = "insert into info1 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # 可以是这样 sql2 = "insert into " +table_name+ " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # 原因是这样的          ↓  这个位置需要传入的类型不能是字符串，需要是列表、元祖等类型
            cursor.execute(sql2, value1)

print("excel to mysql : OK！ ^_^")

# 下面是Excel文件的通过Python输出的数据。
#('id', 'ip', 'port_id', 'scanned_ts', 'protocol', 'state', 'reason', 'reason_ttl', 'service', 'banner', 'title')
#(1, '172.16.2.132', 80, datetime.datetime(2019, 7, 25, 7, 54, 23, 999996), 'tcp', 'open', 'syn-ack', 128, '', '', '')
#(2, '172.16.2.72', 21, datetime.datetime(2019, 7, 25, 7, 54, 23, 999996), 'tcp', 'open', 'response', 128, 'ftp', '220 (vsFTPd 2.2.2)\\x0a530 Please login with USER and PASS.', '')
#(3, '172.16.2.61', 80, datetime.datetime(2019, 7, 25, 7, 54, 35, 3), 'tcp', 'open', 'response', 128, 'http', 'HTTP/1.1 302 Found\\x0d\\x0aDate: Thu, 25 Jul 2019 07:54:26 GMT\\x0d\\x0aServer: Apache/2.4.6 (CentOS) PHP/7.0.23\\x0d\\x0aX-Powered-By: PHP/7.0.23\\x0d\\x0aSet-Cookie: PHPSESSID=vgku95s934f9d7qpte4ai8ofr4; path=/; HttpOnly\\x0d\\x0aCache-Control: no-store, no-cache, must-revalidate\\x0d\\x0aLast-Modified: Thu, 25 Jul 2019 07:54:26 GMT\\x0d\\x0aX-Content-Type-Options: nosniff\\x0d\\x0aExpires: Thu, 25 Jul 2019 07:54:26 GMT\\x0d\\x0aX-Frame-Options: DENY\\x0d\\x0aContent-Security-Policy: default-src \\x27self\\x27; frame-ancestors \\x27none\\x27; style-src \\x27self\\x27 \\x27unsafe-inline\\x27; script-src \\x27self\\x27; img-src \\x27self\\x27\\x0d\\x0aLocation: http://pms.cloudsky.com/login_page.php\\x0d\\x0aContent-Length: 0\\x0d\\x0aConnection: close\\x0d\\x0aContent-Type: text/html; charset=utf-8\\x0d\\x0a\\x0d', '')
