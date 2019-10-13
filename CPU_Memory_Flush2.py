# -*- coding:utf-8 -*-
#original author:Quan Zou
# 链接：https://www.zhihu.com/question/21100416/answer/53430644
# 参考：https://docs.microsoft.com/en-us/windows/console/setconsolecursorposition?redirectedfrom=MSDN
# python             3.7.3
# psutil             5.6.3
#
# 实时监控系统的内存占用率和CPU占用率,两行显示，并刷新。
# 另一种方式的实现：
#    通过Windows API来实现，网上的教程大都是改Win控制台颜色的，但是控制位置的API也是有的。

import ctypes
import psutil
import os
import time
import sys

#获取当前运行的pid
p1=psutil.Process(os.getpid()) 

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

# GetStdHandle：检索指定标准设备（标准输入，标准输出或标准错误）的句柄。
STD_OUTPUT_HANDLE= -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

# 一个COORD结构，以字符为单位指定新的光标位置。坐标是屏幕缓冲区字符单元格的列和行。坐标必须在控制台屏幕缓冲区的边界内。
dwCursorPosition = COORD()
# 下面这两行就是设置刷新的位置了，但是有个问题，如果第4行、第0列，如果原先就有数据，则会覆盖掉，但其他位置的不会受影响。
dwCursorPosition.X = 0
dwCursorPosition.Y = 4

#                          ↓ SetConsoleCursorPosition：设置光标在指定控制台屏幕缓冲区中的位置。
ctypes.windll.kernel32.SetConsoleCursorPosition(std_out_handle,dwCursorPosition)
i=1
while True:
    memory = psutil.virtual_memory().percent  #内存占用率
    cpu = psutil.cpu_percent(interval=1.0) #cpu占用率

    print('#'*22)
    print('## 内存占用率:' + str(memory) + '% ##' + '\n' + '## CPU 占用率:' + str(cpu) + '% ##')
    print('#'*22)
    # print(i)
    # i += 1
    ctypes.windll.kernel32.SetConsoleCursorPosition(std_out_handle,dwCursorPosition)
exit()
