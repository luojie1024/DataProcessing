# -*- coding: utf-8 -*-
'''
# @Time    : 6/1/18 12:18 PM
# @Author  : luojie
# @File    : CarStandHandle.py
# @Desc    : 提取1988-2010标准化技术委员会所在单位名称
'''

import pandas as pd
import numpy as np

basePath = 'data/'

fileName1 = basePath + '1988-1992第一界汽车产业标准化技术委员会.xlsx'
fileName2 = basePath + '1993-2003第二界汽车产业标准化技术委员会.xlsx'
fileName3 = basePath + '2004-2010第三界汽车产业标准化技术委员会.xlsx'
fileName4 = basePath + '20180517汽车产业面板数据组织名单.xlsx'

df = pd.read_excel(fileName1)
# df = df['所在单位']

df3 = pd.read_excel(fileName3, sheet_name=3)

# 合并1988~2003的单位数据
for i in range(6):
    df2 = pd.read_excel(fileName2, sheet_name=i)
    df = pd.concat([df, df2])

# 合并1988~2010的单位数据
for i in range(4):
    df3 = pd.read_excel(fileName3, sheet_name=i)
    df = pd.concat([df, df3])

print('原始数据长度=%d' % len(df))
# 去重
df = df.drop_duplicates(['所在单位'])
print('去重后数据长度=%d' % len(df))

# 抽取所在單位列
df = df['所在单位']

# 保存单位数据
fileName = 'result/1988-2010标准化技术委员会所在单位名称.xlsx'
df.to_excel(fileName,header=True)
print('保存成功!')


# 处理20180517汽车产业面板数据组织名单数据
df = pd.read_excel(fileName4)
# 抽取所在單位列
df = df['OGNM']
# 保存单位数据
fileName = 'result/20180517汽车产业面板数据组织名单.xlsx'
df.to_excel(fileName,header=True)
print(df)
