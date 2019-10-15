<h2 align="center"><code>Python-Code-Base</code></h2>

<br>
<p align="center">
    <img src="以后再说" 
        alt="Master">
</p>
<br>

<p align="center">
  <a href="https://github.com/songshanyuwu/Python-Code-Base">
    <img src="https://img.shields.io/badge/Branch-master-green.svg?longCache=true"
        alt="Branch">

  <a href="http://www.gnu.org/licenses/">
    <img src="https://img.shields.io/badge/License-GNU-blue.svg?longCache=true"
        alt="License">
  </a>
</p>


****

# 目标
个人学习的积累

## 关于



## CUP和内存使用率的监控/刷新显示

- [x] [CPU_Memory_Monitoring.py](https://github.com/songshanyuwu/Python-Code-Base/CPU_Memory_Monitoring.py)
- [x] [CPU_Memory_Flush.py](https://github.com/songshanyuwu/Python-Code-Base/CPU_Memory_Flush.py)
- [x] [CPU_Memory_Flush2.py](https://github.com/songshanyuwu/Python-Code-Base/CPU_Memory_Flush2.py)


## 天气和PM2.5的查询
- [x] [weatherAndPM.py](https://github.com/songshanyuwu/Python-Code-Base/weatherAndPM.py)
- [x] [weatherAndPM_GUI.py](https://github.com/songshanyuwu/Python-Code-Base/weatherAndPM_GUI.py)


## Excel文件的读写/Excel←→MySQL数据传输
- [x] [redayexcel.py](https://github.com/songshanyuwu/Python-Code-Base/redayexcel.py)
- [x] [MySQL2Excel.py](https://github.com/songshanyuwu/Python-Code-Base/MySQL2Excel.py)
- [x] [excelToDatabase.py](https://github.com/songshanyuwu/Python-Code-Base/excelToDatabase.py)

python处理excel已经有大量包，主流代表有：
•xlwings：简单强大，可替代VBA
•openpyxl：简单易用，功能广泛；（可读写excel表）专门处理Excel2007及以上版本产生的xlsx文件，xls和xlsx之间转换容易
•pandas：使用需要结合其他库，数据处理是pandas立身之本
•win32com：不仅仅是excel，可以处理office;不过它相当于是 windows COM 的封装，新手使用起来略有些痛苦。
•Xlsxwriter：丰富多样的特性，缺点是不能打开/修改已有文件，意味着使用 xlsxwriter 需要从零开始。
•DataNitro：作为插件内嵌到excel中，可替代VBA，在excel中优雅的使用python
•xlutils：结合xlrd/xlwt，老牌python包，需要注意的是你必须同时安装这三个库
<img src="https://images2017.cnblogs.com/blog/846822/201709/846822-20170922180351790-690554626.png">
<img src="https://images2017.cnblogs.com/blog/846822/201709/846822-20170922180359743-270272669.png">
最重要的三种：
NULL空值：对应于python中的None，表示这个cell里面没有数据。
numberic： 数字型，统一按照浮点数来进行处理。对应于python中的float。
string： 字符串型，对应于python中的unicode。
Excel文件三个对象
workbook： 工作簿，一个excel文件包含多个sheet。
sheet：工作表，一个workbook有多个，表名识别，如“sheet1”,“sheet2”等。
cell： 单元格，存储数据对象



## 其他杂项
- [x] [directory_tree_count.py](https://github.com/songshanyuwu/Python-Code-Base/directory_tree_count.py)


## 注意：
- 本项目仅用于学习和交流
> 欢迎任何人参与和完善：一个人可以走的很快，但是一群人却可以走的更远
> Thanks for al

