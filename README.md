# Python-Code-Base
个人学习的积累


https://blog.csdn.net/test_soy/article/details/79714858<br>
python处理excel已经有大量包，主流代表有：
•xlwings：简单强大，可替代VBA
•openpyxl：简单易用，功能广泛
•pandas：使用需要结合其他库，数据处理是pandas立身之本
•win32com：不仅仅是excel，可以处理office;不过它相当于是 windows COM 的封装，新手使用起来略有些痛苦。
•Xlsxwriter：丰富多样的特性，缺点是不能打开/修改已有文件，意味着使用 xlsxwriter 需要从零开始。
•DataNitro：作为插件内嵌到excel中，可替代VBA，在excel中优雅的使用python
•xlutils：结合xlrd/xlwt，老牌python包，需要注意的是你必须同时安装这三个库

https://images2017.cnblogs.com/blog/846822/201709/846822-20170922180351790-690554626.png
https://images2017.cnblogs.com/blog/846822/201709/846822-20170922180359743-270272669.png

openpyxl的使用
openpyxl（可读写excel表）专门处理Excel2007及以上版本产生的xlsx文件，xls和xlsx之间转换容易

注意：如果文字编码是“gb2312” 读取后就会显示乱码，请先转成Unicode

 

openpyxl定义多种数据格式
最重要的三种：
NULL空值：对应于python中的None，表示这个cell里面没有数据。
numberic： 数字型，统一按照浮点数来进行处理。对应于python中的float。
string： 字符串型，对应于python中的unicode。
Excel文件三个对象
workbook： 工作簿，一个excel文件包含多个sheet。
sheet：工作表，一个workbook有多个，表名识别，如“sheet1”,“sheet2”等。
cell： 单元格，存储数据对象
1创建一个workbook（工作簿）
wb = Workbook()  # 一个工作簿(workbook)在创建的时候同时至少也新建了一张工作表(worksheet)。

 

2 打开一个已有的workbook：
 wb = load_workbook('file_name.xlsx')
3 打开sheet：
通过名字
    ws = wb["frequency"] 或ws2 = wb.get_sheet_by_name('frequency')
 
不知道名字用index
    sheet_names = wb.get_sheet_names()  #
方法得到工作簿的所有工作表
    ws = wb.get_sheet_by_name(sheet_names[index])# index为0为第一张表 
或者（调用得到正在运行的工作表）

    ws =wb.active或ws = wb.get_active_sheet() #通过_active_sheet_index设定读取的表，默认0读第一个表
    活动表表名wb.get_active_sheet().title
4 新建sheet（工作表）
ws1 = wb.create_sheet() #默认插在最后
ws2 = wb.create_sheet(0) #插在开头 ，
在创建工作表的时候系统自动命名，依次为Sheet, Sheet1, Sheet2 ...
 
ws.title = "New Title" #修改表名称
简化 ws2 = wb.create_sheet(title="Pi")
5 读写单元格
当一个工作表被创建时，其中是不包含单元格。只有当单元格被获取时才被创建。这种方式下，我们不会创建我们使用不到的单元格，从而减少了内存消耗。

 

可以直接根据单元格的索引直接获得
c = ws['A4']     #读取单元格，
如果不存在将在A4新建一个
 
可以通过cell()
方法获取单元格(
行号列号从1开始
)
d = ws.cell(row = 4, column = 2) #通过行列读
d = ws.cell('A4')
 
写入单元格（cell）值
ws['A4'] = 4      #写单元格 
ws.cell(row = 4, column = 2).value = 'test'
ws.cell(row = 4, column = 2, value = 'test')
6 访问多个单元格
cell_range = ws['A1':'C2']    #
使用切片获取多个单元格
 
get_cell_collection()     #读所有单元格数据
7 按行、按列操作
逐行读
 ws.iter_rows(range_string=None, row_offset=0, column_offset=0) #返回一个生成器,
 获得多个单元格
