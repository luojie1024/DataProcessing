# -*- coding: utf-8 -*-
'''
# @Time    : 6/1/18 1:12 PM
# @Author  : luojie
# @File    : CosSimilarity.py
# @Desc    : 相似度计算
'''
import difflib
import pandas as pd
import random
import copy


clear_list = ['有限责任公司', '《', '》', '有限公司', '公司']

pro_list = ['北京', '天津', '河北', '山西', '内蒙',
            '辽宁', '吉林', '黑龙江', '上海', '江苏',
            '浙江', '安徽', '福建', '江西', '山东',
            '河南', '湖北', '湖南', '广东', '广西',
            '四川', '贵州', '云南', '西藏', '陕西',
            '甘肃', '青海', '宁夏', '新疆', '海南',
            '宁波', '广州', '武汉', '重庆', '西安',
            '沈阳', '大连', '哈尔滨', '深圳', '青岛',
            '台湾', '香港', '中国', '0', '1', '2',
            '3', '4', '5', '6', '7', '8', '9',
            '长沙','长春','芜湖','南平','长春','公务','公路']

special_word = '!@#$%^&*)qwertyuiopasdfghjklzxcvbnm⧀⧁⧂⧃⧄⧅⧆⧇⧈⧉⧊⧋⧌⧍⧎⧏⧐⧑⧒⧓⧔⧕⧖⧗⧘⧙⧚⧛⧜⧝⧞⧟'


def str_handle(row1, row2):
    '''
    去除影响词
    :param row1:词1
    :param row2:词2
    :return: 返回处理后的词
    '''
    # clear_list = ['有限责任公司', '《', '》', '有限公司', '公司','中国']
    # 消除
    for i in range(0, len(clear_list)):
        row1 = row1.replace(clear_list[i], '', 3)
        row2 = row2.replace(clear_list[i], '', 3)
    # 置换
    row1 = number_handle(row1)
    row2 = number_handle(row2)
    # 填充
    for i in range(0, len(pro_list)):
        row1 = row1.replace(pro_list[i], get_random_str(7), 3)
        row2 = row2.replace(pro_list[i], get_random_str(7), 3)

    return row1, row2


def number_handle(row):
    '''
    數字轉換
    :param row: 数字
    :return: 转换后的数字
    '''
    row = row.replace('一', '1', 3)
    row = row.replace('二', '2', 3)
    row = row.replace('三', '3', 3)
    row = row.replace('四', '4', 3)
    row = row.replace('五', '5', 3)
    row = row.replace('六', '6', 3)
    row = row.replace('七', '7', 3)
    row = row.replace('八', '8', 3)
    row = row.replace('九', '9', 3)
    row = row.replace('○', '0', 3)
    return row


def get_random_str(len):
    '''
    :param len:随机长度
    :return: 获得随机字符串
    '''
    result = ''
    for i in range(len):#34+32
        index = random.randint(0, 64)
        result += special_word[index]
    return result


random_word_list = []

for x in range(len(pro_list)):
    random_word_list.append(get_random_str(10))

pro_dic = dict(zip(pro_list, random_word_list))

print(pro_list)

# 路径
basePath = 'result/'

fileName1 = basePath + '1988-2010标准化技术委员会所在单位名称.xlsx'
fileName2 = basePath + '20180517汽车产业面板数据组织名单.xlsx'

# 读取文件
df1 = pd.read_excel(fileName1)
df1 = df1['所在单位']

df2 = pd.read_excel(fileName2)
df2 = df2['OGNM']

# 存储组织名称
standOrgName = []
dataOrgName = []
similarScore = []

# 计算组织名称进行相似度分析
for i in df1.index:
    print('\n########OGNM%d##########\n' % i)
    for j in df2.index:
        row1 = copy.deepcopy(str(df1[i]))
        row2 = copy.deepcopy(str(df2[j]))
        # 预处理
        row1, row2 = str_handle(row1, row2)
        # 相似度评估
        slimilarity = difflib.SequenceMatcher(None, row1, row2).quick_ratio()
        if slimilarity > 0.1:
            # 保存
            standOrgName.append(str(df1[i]))
            dataOrgName.append(str(df2[j]))
            similarScore.append(str(slimilarity*100)+'%')
        if slimilarity > 0.6:
            print('\n%s\n%s ,slimilarity=%f\n' % (row1, row2, slimilarity))

# 构建结果集
df = pd.DataFrame({'1988-2010标准化技术委员会所在单位名称': standOrgName,
                   '20180517汽车产业面板数据组织名单': dataOrgName,
                   '相似度': similarScore
                   }, )

# 去重
df = df.drop_duplicates(['1988-2010标准化技术委员会所在单位名称', '20180517汽车产业面板数据组织名单'])

# 排序
df = df.sort_values(by=['相似度'], ascending=False)

# 保存
filename = 'result/标准化vs面板数据(相似度分析).xlsx'
df.to_excel(filename)

# 存储相互间组织名称
standOrgName2 = []
dataOrgName2 = []
similarScore2 = []

index = df1.index[0]

# 组织名之间的相似度
for i in df1.index:
    row1 = copy.deepcopy(str(df1[index]))
    row2 = copy.deepcopy(str(df1[i]))
    if row1 == row2:
        continue
    # 预处理
    row1, row2 = str_handle(row1, row2)
    # 相似度评估
    slimilarity = difflib.SequenceMatcher(None, row1, row2).quick_ratio()
    if slimilarity > 0.1:
        # 保存
        standOrgName2.append(str(df1[i]))
        dataOrgName2.append(str(df1[index]))
        similarScore2.append(str(slimilarity*100)+'%')
    if slimilarity > 0.6:
        print('\n%s\n%s ,slimilarity=%f\n' % (row1, row2, slimilarity))
    index = i

# 构建结果集
df = pd.DataFrame({'单位名称1': standOrgName2,
                   '单位名称2': dataOrgName2,
                   '相似度': similarScore2
                   }, )

# 去重
df = df.drop_duplicates(['单位名称1', '单位名称2'])

# 排序
df = df.sort_values(by=['相似度'], ascending=False)

# 保存
filename = 'result/标准化vs标准化(相似度分析).xlsx'
df.to_excel(filename)

# 存储相互间组织名称
standOrgName2 = []
dataOrgName2 = []
similarScore2 = []

# 组织名之间的相似度
for i in df2.index:
    row1 = copy.deepcopy(str(df2[index]))
    row2 = copy.deepcopy(str(df2[i]))
    if row1 == row2:
        continue
    # 预处理
    row1, row2 = str_handle(row1, row2)
    # 相似度评估
    slimilarity = difflib.SequenceMatcher(None, row1, row2).quick_ratio()
    if slimilarity > 0.1:
        # 保存
        standOrgName2.append(str(df2[i]))
        dataOrgName2.append(str(df2[index]))
        similarScore2.append(str(slimilarity*100)+'%')
    if slimilarity > 0.6:
        print('\n%s\n%s ,slimilarity=%f\n' % (row1, row2, slimilarity))
    index = i

# 构建结果集
df = pd.DataFrame({'单位名称1': standOrgName2,
                   '单位名称2': dataOrgName2,
                   '相似度': similarScore2
                   }, )

# 去重
df = df.drop_duplicates(['单位名称1', '单位名称2'])

# 排序
df = df.sort_values(by=['相似度'], ascending=False)

# 保存
filename = 'result/面板数据vs面板数据(相似度分析).xlsx'
df.to_excel(filename)
