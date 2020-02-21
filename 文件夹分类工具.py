# -*- coding: utf-8 -*-
# author:songshanyuwu
# 2020.02.21 
# V1.0

import sys,os
from pathlib import Path
import shutil

# 路径结构介绍：
# |----月报分类工具.py        ←主程序
# |----config.txt            ←配置文件，用于修改分组，英文逗号分隔，不要有空格、空行
# |----未分类\                 ←没有分类的150+家企业月报
#     |----目录1-1\
#     |    |----文件1-1-1.docx
#     |    |----文件1-1-2.xlsx
# 
# |----分类\                  ←该目录为程序自动创建，并将企业月报移动分类
#     |----分类目录2-1\
#         |----目录1-1\
#         |    |----文件1-1-1.docx
#         |    |----文件1-1-2.xlsx

# config.txt 文件内容格式如下：
# 英文逗号分隔，不要有空格、空行,一般不需要调整
#用于创建分类二级目录的名称,未分类目录下的文件夹名称

# # 食用方法：
# 同样可以使用以下命令进行测试：
# python dirtree.py C:\Users\root\Desktop\月报自动分类\月报文件分类工具\未分类


def moveDirectory(targetPath):
    # 获取待处理的 Path 对象，使用pathlib模块操作
    # targetPath = Path('C:\\Users\\root\\Desktop\\月报自动分类\\未分类')
    targetPath = Path(targetPath)
    # 处理得到父目录的路径
    originPath= str(targetPath)[0:-len(targetPath.name)]
    print('12',targetPath)
    # 读取配置文件，获得对比值
    comparisonList = {}
    directory = []
    if Path(originPath + 'config.txt').exists:
        print('配置文件加载中...')
    else:
        print('缺少配置文件，请检查...')
        sys.exit(0)
    with open(originPath + 'config.txt', 'r', encoding='utf-8' ) as cfg:
        for line in cfg.readlines():
            comparisonList[line.split(',')[1].replace("\n", "")] = line.split(',')[0]
            if line.split(',')[0] in directory:
                pass
            else:
                directory.append(line.split(',')[0])
    # 检查字典是否正确
    # for key ,value in comparisonList.items():
    #     print('key',key)
    #     print('value',value)
    # 检查列表directory是否正确
    # print(directory)

    # 创建处理后的目录，使用pathlib模块操作
    for i in directory:
        resultPath = originPath+'分类/' + i
        Path(resultPath).mkdir(parents=True)

    # 获取待处理目录下的所有目录，使用pathlib模块操作
    # targetPath.iterdir()

    # 判断是文件还是目录，使用pathlib模块操作
    i = 0
    for line in targetPath.iterdir():
        if line.is_file():
            print(str(line)+'————是文件')
        elif line.is_dir():
            # print(str(line)+'————是目录')
            fileName = line.name.split('_')[-3]
            if fileName in comparisonList.keys():
                # print('存在',fileName)
                # print(Path(line))
                # print(Path(originPath + '分类\' + comparisonList[fileName] + '\' + line.name))
                src = line
                dst =originPath + '分类\\' + comparisonList[fileName] + '\\' + line.name
                # 使用pathlib模块操作没有成功，改为使用shutil模块操作
                shutil.move(src,dst)
                print('已经移动目录' + fileName)
        i += 1
    print('====已经处理' + str(i) + '个目录====')


if __name__ == '__main__':
    # dirtree = DirectionTree()
    # 命令参数个数为2，开始分类作业
    if len(sys.argv) == 2 and Path(sys.argv[1]).exists():
        moveDirectory(sys.argv[1])
    else:  # 参数个数太多，无法解析
        print('命令行参数不对，请检查！')
