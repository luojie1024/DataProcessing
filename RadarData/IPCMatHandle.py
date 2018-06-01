# -*- coding: utf-8 -*-
'''
# @Time    : 5/18/18 8:52 PM
# @Author  : luojie
# @File    : IPCMatHandle.py.py
# @Desc    : IPC mat生成
'''
import pandas as pd
import numpy as np
import logging

# ipc长度
ipc_len = 1


def standard_coupling_mat(ipc_count_dict, ipc_list, orgin_mat, handle_mat):
    '''
    :param ipc_count_dict:ipc統計數量
    :param ipc_count_dict_keys:统计键列表
    :param orgin_mat:耦合关系矩阵
    :param handle_mat:标准化后的关系阵
    :return:标准化后的关系阵
    '''
    x = handle_mat.shape[0]
    y = handle_mat.shape[1]
    for i in range(0, x):
        for j in range(i, y):
            if orgin_mat[i][j] < 1:
                temp = 0.0
            else:
                temp = (orgin_mat[i][j] / (
                        float(ipc_count_dict[ipc_list[j]]) + float(ipc_count_dict[ipc_list[i]]) - orgin_mat[i][j]))
            handle_mat[i][j] = temp
            handle_mat[j][i] = temp
    return handle_mat


def handle_coupling_mat(coupling_lists, orgin_mat):
    '''
    处理耦合矩阵
    :param coupling_lists: 耦合关系列
    :param orgin_mat: 耦合阵
    :return:
    '''
    # 临时耦合矩阵,防止重复统计
    for coupling_list in coupling_lists:
        temp_mat = np.zeros(orgin_mat.shape, dtype=np.float)
        temp_mat = handle_coupling(coupling_list, temp_mat)
        # 耦合矩阵累加
        orgin_mat = np.add(orgin_mat, temp_mat)
    return orgin_mat


def handle_coupling(coupling_list, temp_mat):
    '''
    处理耦合关系
    :param coupling_list: 耦合关系
    :param temp_mat:暫存耦合阵
    :return:暫存耦合关系
    '''
    it_len = len(coupling_list)
    for i in range(0, it_len - 1):
        for j in range(i + 1, it_len):
            # 获取IPC号
            x = coupling_list[i][0:ipc_len]
            y = coupling_list[j][0:ipc_len]
            # 转化索引
            x = get_ipc_index(x)
            y = get_ipc_index(y)
            # 防止重復統計
            if temp_mat[x][y] < 1:
                # 耦合阵计数
                temp_mat[x][y] = temp_mat[y][x] + 1
            if temp_mat[y][x] < 1:
                # 耦合阵计数
                temp_mat[y][x] = temp_mat[y][x] + 1
            else:
                continue
    return temp_mat


def get_ipc_index(IPC):
    '''
    IPC号转换成索引
    :param IPC: IPC号码
    :return: IPC矩阵位置索引
    '''
    return ipc_index_dic[IPC]


def create_coupling_lists(df, coupling_lists, ipc_count_dict):
    '''
    :param df: 数据集
    :param coupling_lists: 耦合关系列表
    :param ipc_count_dict: ipc数量列表
    :return: 返回统计后的耦合关系列表和ipc数量列表
    '''
    # 遍历分类号,各个专利出现数量
    for index in df.index:
        temp_str = df[index]
        # 如果出现多个专利
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

            safe_list = []
            # 记录个类型出现次数
            for i in range(len(list_id)):
                if list_id[i][0:ipc_len] in ipc_count_dict.keys():
                    ipc_count_dict[list_id[i][0:ipc_len]] = ipc_count_dict[list_id[i][0:ipc_len]] + 1
                    safe_list.append(list_id[i])
                else:
                    print('error data=%s' % list_id[i])
                    continue
            # 保存关系列表
            coupling_lists.append(safe_list)
        else:
            # 计数++
            ipc_count_dict[temp_str[0:ipc_len]] = ipc_count_dict[temp_str[0:ipc_len]] + 1

    return coupling_lists, ipc_count_dict


logging.basicConfig(filename='log/mat_handle_log_info.log', level=logging.INFO)

logging.info('\n####################step1-读取IPC列表########################################\n')

# 一位IPC
excel_path = 'data/class_id_' + str(ipc_len) + '.xlsx'
df = pd.read_excel(excel_path, names=['分类号'])

df = df['分类号']

logging.info('\n####################step2-创建IPC矩阵########################################\n')

# 构建ipc列表
ipc_list = []
ipc_tup = ()

# 获取IPC列表
for index in df.index:
    ipc_list.append(df[index])

# 构建索引字典
ipc_index_dic = dict(zip(ipc_list, [x for x in range(len(ipc_list))]))

# 构建26期数据
for time in range(1985, 2012):
    # 构建数量字典
    ipc_count_dict = dict(zip(ipc_list, [0.0] * len(ipc_list)))

    filename = 'data/' + str(time) + '.xlsx'
    df1 = pd.read_excel(filename)
    df1 = df1['分类号']
    filename = 'data/' + str(time + 1) + '.xlsx'
    df2 = pd.read_excel(filename)
    df2 = df2['分类号']
    filename = 'data/' + str(time + 2) + '.xlsx'
    df3 = pd.read_excel(filename)
    df3 = df3['分类号']
    df = pd.concat([df1, df2, df3])
    print('df1_len=%d,df2_len=%d,df3_len=%d\n' % (len(df1), len(df2), len(df3)))
    print('df=%d' % (len(df)))

    # 获取不合格数据列
    for index in df.index:
        delete_list = []
        row = df[index]
        if row[0:ipc_len] not in ipc_count_dict.keys():
            delete_list.append(index)
            print(row)

    # 刪除不合格數據
    if len(delete_list) > 0:
        # 删除不合格数据
        df = df.drop(delete_list)
        print('delete len =%d' % len(delete_list))

    # 构建初始耦合阵
    orgin_mat = np.zeros([len(ipc_index_dic.keys()), len(ipc_index_dic.keys())], dtype=np.float)
    handle_mat = np.zeros([len(ipc_index_dic.keys()), len(ipc_index_dic.keys())], dtype=np.float)

    # 耦合列表
    coupling_lists = []

    # 創建耦合關系列表和ipc統計字典
    coupling_lists, ipc_count_dict = create_coupling_lists(df, coupling_lists, ipc_count_dict)

    print('###############orgin_mat###############')
    print(orgin_mat)
    # 生成耦合矩阵
    orgin_mat = handle_coupling_mat(coupling_lists, orgin_mat)
    # 获得标准化后的关系阵
    handle_mat = standard_coupling_mat(ipc_count_dict, ipc_list, orgin_mat, handle_mat)
    print('###############after_mat###############')

    # 构建文件DataFrame
    df1 = pd.DataFrame(orgin_mat, columns=ipc_index_dic.keys(), index=ipc_index_dic.keys())
    df2 = pd.DataFrame(handle_mat, columns=ipc_index_dic.keys(), index=ipc_index_dic.keys())
    print(df1)
    print('-------------------------------------')
    print(df2)

    # 保存文件
    filename = 'result/original/' + str(time) + '-' + str(time + 2) + 'IPC' + str(ipc_len) + '.xlsx'
    df1.to_excel(filename, header=True)
    filename = 'result/standardization/' + str(time) + '-' + str(time + 2) + 'IPC' + str(ipc_len) + '.xlsx'
    df2.to_excel(filename, header=True)
    print('\n\n....%s\n\n' % filename)