# -*- coding: utf-8 -*-
'''
# @Time    : 5/18/18 1:51 PM
# @Author  : luojie
# @File    : IPCHandle.py.py
# @Desc    : IPC 获取
'''
import pandas as pd
import numpy as np
import logging

logging.basicConfig(filename='log/mat_log_info.log', level=logging.INFO)

excel_path = 'data/处理后1985_2013.xlsx'

logging.info('####################step1-获取IPC号列表########################################\n')
df = pd.read_excel(excel_path)

df = df['分类号']

print(df.head(10))

list_class_id = []

# 遍历获取全部出现过的id
logging.info('/n############处理异常数据############/n')
for index in df.index:
    temp_str = str(df.loc[index])
    # 如果存在多个分类号
    if ';' in temp_str:
        list_id = []
        if ',' in temp_str:  # 存在多种分隔符
            temp_list_id = temp_str.split(';')
            # 处理逗号分隔符
            for index in range(len(temp_list_id)):
                if ',' in temp_list_id[index]:
                    list_id.extend(temp_list_id[index].split(','))
                else:
                    list_id.append(temp_list_id[index])
            print('list_len=%d' % len(list_id))
            # 处理异常数据
            for index in range(len(list_id)):
                if '//' in list_id[index][0:2]:
                    list_id[index] = list_id[index][2:]
                if '(' in list_id[index][0:1]:
                    list_id[index] = list_id[index][1:]
        else:  # 只有;分隔符
            list_id = temp_str.split(';')
            # 处理异常数据
            for index in range(len(list_id)):
                if '//' in list_id[index][0:2]:
                    list_id[index] = list_id[index][2:]
                if '(' in list_id[index][0:1]:
                    list_id[index] = list_id[index][1:]
        list_class_id.extend(list_id)
    else:
        list_class_id.append(temp_str)

logging.info('/n############处理//符号############/n')
logging.info('/n############处理(符号############/n')
print('\n遍历出分类号:\n')

# id 列表
df_id = pd.DataFrame({'分类号': list_class_id})

print(df_id.head(10))

print('\n分类号去重:\n')
# 按分类号去重
df_id = df_id.drop_duplicates(['分类号'])
print(df_id.head(10))

dict_1 = []
dict_3 = []
dict_4 = []

logging.info('\n####################step2-按长度截取IPC########################################\n')

print('\n按长度截取分类号:\n')
for index in df_id.index:
    temp_str = str(df_id.loc[index]['分类号'])
    if temp_str[0].isalpha():
        print(temp_str)
        dict_1.append(temp_str[0:1])
        dict_3.append(temp_str[0:3])
        dict_4.append(temp_str[0:4])
    else:
        print('<-------不合法数据%s-------->'%temp_str)

logging.info('\n####################step3-IPC去重########################################\n')

df1 = pd.DataFrame({'分类号': dict_1})
df3 = pd.DataFrame({'分类号': dict_3})
df4 = pd.DataFrame({'分类号': dict_4})


df1 = df1.drop_duplicates(['分类号'])
df1 = df1.sort_values(['分类号'])
df3 = df3.drop_duplicates(['分类号'])
df3 = df3.sort_values(['分类号'])
df4 = df4.drop_duplicates(['分类号'])
df4 = df4.sort_values(['分类号'])

logging.info('\n####################step4-按长度截取IPC########################################\n')

filename = 'data/class_id_1.xlsx'
df1.to_excel(filename, header=True,columns=['分类号'])
filename = 'data/class_id_3.xlsx'
df3.to_excel(filename, header=True,columns=['分类号'])
filename = 'data/class_id_4.xlsx'
df4.to_excel(filename, header=True,columns=['分类号'])
