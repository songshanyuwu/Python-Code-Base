# -*- coding:utf-8 -*-
#original author: ***
# 链接：http://blog.chinaunix.net/uid-21374062-id-5198995.html
# 参考：
# python             3.7.3
# 
#
#countFile.py
# 仿Linux树形目录结构并汇总当前目录下文件总数


import os  

def fileCntIn(currPath):  
    '''汇总当前目录下文件数'''  
    return sum([len(files) for root, dirs, files in os.walk(currPath)])  
  
def dirsTree(startPath):  
    '''树形打印出目录结构'''  
    for root, dirs, files in os.walk(startPath):  
        #获取当前目录下文件数  
        fileCount = fileCntIn(root)  
        #获取当前目录相对输入目录的层级关系,整数类型  
        level = root.replace(startPath, '').count(os.sep)  
        #树形结构显示关键语句  
        #根据目录的层级关系，重复显示'| '间隔符，  
        #第一层 '| '  
        #第二层 '| | '  
        #第三层 '| | | '  
        #依此类推...  
        #在每一层结束时，合并输出 '|____'  
        indent = '|   ' * 1 * level + '|____'  
        print('%s%s -r:%s' % (indent, os.path.split(root)[1], fileCount))  
        for file in files:
            indent = '|   ' * 1 * (level+1) + '|____'  
            print('%s%s' % (indent, file))
  
if __name__ == '__main__':  
    #path = u"D:\\影像备份\\照片" 
    path = os.getcwd()   #当前目录
    dirsTree(path)

#  判断Path是不是目录    
# os.path.isdir(childPath)

# 统计文件夹下文件（含文件夹）的个数
# len(os.listdir(DIR))
