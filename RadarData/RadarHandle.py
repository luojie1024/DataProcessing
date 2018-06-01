# -*- coding: utf-8 -*-
'''
# @Time    : 5/17/18 1:06 PM
# @Author  : luojie
# @File    : RadarHandle.py
# @Desc    : 雷达数据处理
'''

import pandas as pd
import numpy as np
import re
from datetime import datetime
from datetime import timedelta
import logging

logging.basicConfig(filename='log/log_info.log', level=logging.INFO)

excel_path = "data/1985_2011.xlsx"
df_xls = pd.read_excel(excel_path)

province_dic = {'11': '北京', '12': '天津', '13': '河北', '14': '山西', '15': '内蒙',
                '21': '辽宁', '22': '吉林', '23': '黑龙江', '31': '上海', '32': '江苏',
                '33': '浙江', '34': '安徽', '35': '福建', '36': '江西', '37': '山东',
                '41': '河南', '42': '湖北', '43': '湖南', '44': '广东', '45': '广西',
                '51': '四川', '52': '贵州', '53': '云南', '54': '西藏', '61': '陕西',
                '62': '甘肃', '63': '青海', '64': '宁夏', '65': '新疆', '66': '海南',
                '97': '宁波', '81': '广州', '83': '武汉', '85': '重庆', '87': '西安',
                '89': '沈阳', '91': '大连', '93': '哈尔滨', '94': '深圳', '95': '青岛',
                # '71': '台湾', 'HK': '香港'
                }

province_id = province_dic.keys()

logging.info('####################step1-数据去重留公开日最新数据########################################')
logging.info('\n处理前数据长度:%d\n', len(df_xls))
logging.info('\n原始数据\n:')
logging.info(df_xls.head())
# 按申请号和公开日期排序
df_xls = df_xls.sort_values(by=['申请号', '公开（公告）日'], ascending=False)
logging.info('\n排序后\n:')
logging.info(df_xls.head())
# 排序后的数据去重
df_xls = df_xls.drop_duplicates(['申请号'])
logging.info('\n去重后\n:')
logging.info(df_xls.head())
logging.info('处理后数据长度:%d\n', len(df_xls))

logging.info('\n####################step2-剔除不在中国大陆的数据########################################')
logging.info('\n处理前数据长度:%d\n\n\n\n', len(df_xls))
del_index = []
for index in df_xls.index:
    # 保存行数据
    row_data = str(df_xls.loc[index]['国省代码'])
    # 判断数据是否缺损
    if len(row_data) >= 2:
        if row_data[-2:] in province_id:
            # logging.info(row_data[0:2])
            pass
        else:
            logging.info('申请号:%s %s 不属于中国大陆' % (str(df_xls.loc[index]['申请号']), str(row_data[0:2])))
            del_index.append(index)
    else:
        logging.info('国省代码值错误:申请号->')
        logging.info(df_xls.loc[index]['申请号'])
# 删除外国专利索引
df_xls = df_xls.drop(del_index)

logging.info('删除外国专利:%d项\n' % len(del_index))
logging.info('处理后数据长度:%d\n' % len(df_xls))

logging.info('####################step3-剔除外观设计专利########################################')
logging.info('处理前数据长度:%d' % len(df_xls))
del_index = []
for index in df_xls.index:
    # 保存行数据
    row_data = str(df_xls.loc[index]['主分类号'])
    # 判断数据是否缺损
    flag = '-'
    if len(row_data) >= 2:
        if row_data.find(flag) >= 0:
            del_index.append(index)
            logging.info('申请号:%s 外观专利主分类号:%s' % (str(df_xls.loc[index]['申请号']), row_data))
    else:
        logging.info('主分类号代码值错误:申请号->')
        logging.info(df_xls.loc[index]['申请号'])
# 删除外国专利索引
df_xls = df_xls.drop(del_index)

logging.info('删除外观设计专利:%d项\n' % len(del_index))

logging.info('处理后数据长度:%d\n' % len(df_xls))

filename = 'data/处理后1985_2013.xlsx'
df_xls.to_excel(filename, header=True)

# logging.info('####################step4-剔除不在中国大陆的数据########################################')
# logging.info('处理前数据长度:%d',len(df_xls))
#
#
# logging.info('处理后数据长度:%d',len(df_xls))


# logging.info(df_xls.head())

# 按申请号和公开日期排序
df_xls = df_xls.sort_values(by=['申请号'], ascending=False)

for year in range(1985, 2014):
    get_indexs = []
    for index in df_xls.index:
        # 保存行数据
        apply_time = str(df_xls.loc[index]['申请号'])
        if year < 2003:
            if apply_time[2:4] == str(year)[2:4]:
                get_indexs.append(index)
        else:
            if apply_time[2:6] == str(year):
                get_indexs.append(index)
    filename = 'data/' + str(year) + '.xlsx'
    df_year = df_xls.loc[get_indexs]
    df_year.to_excel(filename, header=True)
    logging.info('%d_to_excel,len=%d' % (year, len(df_year)))

logging.info(df_xls.head(20))
