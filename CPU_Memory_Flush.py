# -*- coding:utf-8 -*-
# original author: 回形针
# https://www.zhihu.com/question/21100416/answer/208143599
#
# python             3.7.3
# psutil             5.6.3
#
# 实时监控系统的内存占用率和CPU占用率,两行显示，并刷新

import psutil
import os
import time
import sys

#获取当前运行的pid
p1=psutil.Process(os.getpid()) 

while True:
    memory = psutil.virtual_memory().percent  #内存占用率
    cpu = psutil.cpu_percent(interval=1.0) #cpu占用率

    #  第一种方法：print ，失败-_-||
    #print("\r","内存占用率:{:<8}     CPU占用率:{:<8}".format(memory,cpu),end="",flush=True)

    #  第一种方法的变形：print ，失败-_-||
    #c = '内存占用率:' + str(memory) + '\n' + 'CPU占用率:' + str(cpu) 
    #print("\r",'CPU占用率:' + str(cpu),end="",flush=True)

    # 第二种方法：ANSI.SYS,  测试结果，在Linux下成功，Windows下失败
    print('内存占用率:' + str(memory) + '\n' + 'CPU占用率:' + str(cpu))
    time.sleep(2)
    print('\x1b[2J')

    # 第三种方法: 利用sys的标准输出 ，失败-_-||
    # print('内存占用率:' + str(memory) + '\n' + 'CPU占用率:' + str(cpu))
    # sys.stdout.flush()
    # time.sleep(2)

'''
ANSI.SYS 是一个DOS的驱动 ANSI不仅仅能控制终端的光标(而且ANSI本身也可以指代其他的许多东西 在这里特指'ANSI转义码') 
(举个栗子 各种宽字符的cp叫'ANSI字符集'也是ANSI(美国国家标准协会)的标准之一)
PS ANSI的最新标准是ISO/IEC 6429既然是转义符 那么用起来就很方便了 只要像'\n \t \r \b'之类的转义符那样插在文本里print()或者dump()到屏幕上就行   
具体方法如下:ANSI序列以 'ESC字符'+'[' 起始(在纯DOS下双击'ESC'键可获得'ESC字符'*1) 在Python中'ESC字符'可以用'\x1b'来表示 在这之后接具体的控制码即可
        \x1b[nA    光标上移
        \x1b[nB    光标下移
        \x1b[nC    光标右移
        \x1b[nD    光标左移
        (n 为行数/字符数)
        \x1b[2J    清屏(把2换成其他数字会有不同的清屏效果)
        \x1b[x;yH   调整屏幕坐标(x,y的单位是字符)
        \x1b?25l  隐藏光标
        \x1b?25h  显示光标
注1: 这些转义符统统大小写敏感，完整的列表或者高级的使用方法可以去看wiki(用的好的话甚至可以做到按rgb调整颜色)
注2: 所有的指令的生效区间都是字符级的，也就是说甚至可以做到每个字符用不同的颜色和特效(在那个'黑框框'里!!!)
这个方法有个很神奇的操作
    print('\x1b[%dA' % (n))
    print('\x1b[%d%s' % (n,ope))
缺点是不同的终端的支持的程度不同
'''
