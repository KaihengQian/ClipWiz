import pandas as pd
import numpy as np
import math


def str2sec(x):  # 字符串时分秒转换成秒
    h, m, s = x.strip().split(':')  # .split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算


def fulltime(stamp_start, stamp_end):
    full_time = 0
    for i in range(len(stamp_start)):
        full_time += stamp_end[i] - stamp_start[i]
    return full_time


def intersection(our_starttime, our_endtime, stamp_starttime, stamp_endtime):  # 四个参数分别是我们的起始终止时间和标准的起始终止时间；交集函数
    begin = int(max(our_starttime, stamp_starttime))
    end = int(min(our_endtime, stamp_endtime))
    len_intersection = end - begin
    return len_intersection


def union(our_starttime, our_endtime, stamp_starttime, stamp_endtime):  # 四个参数分别是我们的起始终止时间和标准的起始终止时间；并集函数
    begin = int(min(our_starttime, stamp_starttime))
    end = int(max(our_endtime, stamp_endtime))
    len_union = end - begin
    return len_union


def evaluation_function(our_data_path, stamp_data_path, evaluation_path, predict_data_path):  # our_time是一个二维数组 our_time[1][1]代表{our_starttime[1],our_endtime[1]}
    length = []
    weight = []

    stamp_data = pd.read_csv(stamp_data_path, names=["start", "end", "content"])
    stamp_start = np.array(stamp_data["start"])
    stamp_end = np.array(stamp_data["end"])
    for i in range(len(stamp_start)):
        stamp_start[i] = str2sec(stamp_start[i])
        stamp_end[i] = str2sec(stamp_end[i])

    our_data = pd.read_csv(our_data_path)
    our_start = np.array(our_data["start"])
    our_end = np.array(our_data["end"])

    block_intersection= np.zeros(len(stamp_start))  # 保存预测结果与标注的交集
    i = 0
    j = 0
    while i < len(our_start) and j < len(stamp_start):
        if our_start[i] >= stamp_end[j]:
            j += 1
        elif our_end[i] <= stamp_start[j]:
            i += 1
        else:
            intersection_start = max(our_start[i], stamp_start[j])
            intersection_end = min(our_end[i], stamp_end[j])
            intersection = intersection_end - intersection_start
            block_intersection[j] += intersection
            if our_end[i] < stamp_end[j]:
                i += 1
            else:
                j += 1

    for j in range(len(stamp_start)):
        length.append(stamp_end[j] - stamp_start[j])
        if length[j] <= 5:
            weight.append(0)
        elif length[j] <= 10:
            weight.append(1)
        elif length[j] < 15:
            weight.append(2)
        else:
            weight.append(3)

    stamp_data['length'] = length
    stamp_data['weight'] = weight
    stamp_data['block_intersection'] = block_intersection
    stamp_data['score'] = stamp_data['block_intersection'] / stamp_data['length'] * stamp_data['weight']
    stamp_data.to_csv(predict_data_path, index=False)

    score = np.array(stamp_data['score'])
    recall_rate = sum(score) / sum(weight)
    precision_rate = sum(block_intersection) / fulltime(our_start, our_end)
    F_beta = 2 * precision_rate * recall_rate / (precision_rate + recall_rate)

    evaluation = "加权召回率为：  " + str(recall_rate) + "\n" + \
                 "准确率为：  " + str(precision_rate) + "\n" + \
                 "F_beta值为：  " + str(F_beta)
    with open(evaluation_path, "w") as f:
        f.write(evaluation)

    return F_beta
# score = intersection /length * weight
# score_sum/weight_sum
# length weight intersection score
