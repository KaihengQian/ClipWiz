import pandas as pd
import numpy as np
import math


def str2sec(x):  # 字符串时分秒转换成秒
    h, m, s = x.strip().split(':')  # .split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算


def judge(our_starttime, our_endtime, stamp_starttime, stamp_endtime):  # 判断两个时间段是否有交集
    return bool(not(stamp_endtime < our_starttime or stamp_starttime > our_endtime))


def intersection(our_starttime, our_endtime, stamp_starttime, stamp_endtime):  # 四个参数分别是我们的起始终止时间和标准的起始终止时间；交集函数
    begin = min(our_starttime, stamp_starttime)
    end = max(our_endtime, stamp_endtime)
    len_intersection = end - begin
    return len_intersection


def union(our_starttime, our_endtime, stamp_starttime, stamp_endtime):  # 四个参数分别是我们的起始终止时间和标准的起始终止时间；并集函数
    begin = max(our_starttime, stamp_starttime)
    end = min(our_endtime, stamp_endtime)
    len_union = end - begin
    return len_union


def evaluation_function(our_data_path, stamp_data_path):  # our_time是一个二维数组 our_time[1][1]代表{our_starttime[1],our_endtime[1]}
    stamp_data = pd.read_csv(stamp_data_path, header=None)
    stamp_list = stamp_data.values.tolist()
    for i in range(len(stamp_list)):
        stamp_list[i][0] = str2sec(stamp_list[i][0])
        stamp_list[i][1] = str2sec(stamp_list[i][1])

    our_data = pd.read_csv(our_data_path, header=None)
    our_list = our_data.values.tolist()

    length_sum_intersection = 0
    length_sum_union = 0
    for i in range(len(our_list)):
        for j in range(len(stamp_list)):
            if judge(our_list[i][0], our_list[i][1], stamp_list[j][0], stamp_list[j][1]):
                # ength_sum_intersection += intersection(our_list[i][0], our_list[i][1], stamp_list[j][0], stamp_list[j][1])
                length_sum_union += union(our_list[i][0], our_list[i][1], stamp_list[j][0], stamp_list[j][1])
    for i in range(len(our_list)):
        length_sum_intersection += our_list[i][1] - our_list[i][0]
    for j in range(len(stamp_list)):
        length_sum_intersection += stamp_list[j][1] - stamp_list[j][0]
    length_sum_intersection = length_sum_intersection - length_sum_union
    # print(length_sum_intersection)
    # print(length_sum_union)
    print(length_sum_union/length_sum_intersection * 100)
    # return length_sum_intersection

