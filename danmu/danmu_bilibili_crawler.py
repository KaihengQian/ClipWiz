import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
import matplotlib.pyplot as plt
import jieba
import numpy as np
from moviepy import editor


# 定义请求头 request headers
headers = {
    # 'content-type': 'application/x-www-form-urlencoded',
    # 'origin': 'https://www.bilibili.com',
    # 'referer': 'https://www.bilibili.com/variety/?spm_id_from=333.1007.0.0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}


# 判断文本相似性
def jaccard(text1, text2):
    # 将弹幕文本分词后转化为集合
    set1 = set(jieba.lcut(text1))
    set2 = set(jieba.lcut(text2))
    # 求并集与交集
    set_union = set1.union(set2)
    set_intersection = set1.intersection(set2)
    # 计算jaccard系数即交并比
    jaccard_index = len(set_intersection) / len(set_union)
    return jaccard_index


# 通过b站视频链接获取cid并返回
def url_get_cid(bili_url):
    session = HTMLSession()
    res = session.get(bili_url, headers=headers)
    match = re.findall('"backup_url":.*?"https://upos-sz.*?bilivideo.com/upgcxcode/.*?/.*?/(.*?)/.*?/', res.text)
    return match[0]


# 通过bvid即bv号获取视频cid
def bv_get_cid(bv):
    cid_url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bv  # 页面内容较简洁
    res = requests.get(cid_url)
    cid = re.findall(r'"cid":(.*?),', res.text)
    return cid[0]


# 通过cid获取储存弹幕的api接口地址
def cid_to_url(cid):
    cid_dm_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + cid
    return cid_dm_url


# 通过存储弹幕信息的网址获得包含发送时间和弹幕内容的csv文件
def get_dm_to_csv(dm_url, danmu_output_path):
    # 初始化弹幕信息列表
    dm_time = []
    dm_text = []
    dm_user = []
    dm_date = []
    # 获取网址内容
    dm_res = requests.get(dm_url)
    dm_res.encoding = 'utf-8'
    # 解析xml网页,并获取d标签内容(发送用户,时间属性,弹幕内容)
    soup = BeautifulSoup(dm_res.text, 'xml')
    for dm_info in soup.find_all('d'):
        # 三种对发送时间的取值法
        # time = float(dm_info.attrs['p'].split(',')[0]).__round__()  # 四舍五入
        # time = (float(dm_info.attrs['p'].split(',')[0]) - 1).__round__()  #退一法
        time = float(dm_info.attrs['p'].split(',')[0])  # 精确保留
        user = dm_info.attrs['p'].split(',')[6]  # 发送弹幕的用户ID
        date = dm_info.attrs['p'].split(',')[4]  # 用户发送弹幕的日期时间
        # 储存数据
        dm_user.append(user)
        dm_time.append(time)
        dm_date.append(date)
        # dm_text.append(dm_info.text)
        dm_text.append(re.sub(r' ', '', dm_info.text))  # 去除弹幕中的空格
    # 构造DataFrame
    dm = pd.DataFrame()
    dm['user_id'] = dm_user
    dm['timestamp'] = dm_date
    dm['elapse_time'] = dm_time
    dm['text'] = dm_text
    # 写入csv文件
    dm.to_csv(danmu_output_path)
    # # 输出弹幕数量,以作分析
    # print('弹幕数量为')
    # print(len(dm))
    # 清空列表存储内容
    dm_time.clear()
    dm_text.clear()
    dm_user.clear()
    dm_date.clear()


# 同用户相似弹幕噪声去除
def clear_similarities(danmu_input_path, danmu_output_path):
    tmp_dm = pd.read_csv(danmu_input_path)
    group_dm = tmp_dm.groupby('user_id')
    index_to_drop = []
    # 循环处理每一个组
    for name, group in group_dm:
        group_size = len(group)
        # 相同发送用户的弹幕间两两进行判定
        for i in range(group_size):
            for j in range(i + 1, group_size):
                # 判断弹幕相似度,以jaccard系数0.7为阈值
                if (jaccard(group.iloc[i]['text'], group.iloc[j]['text']) > 0.7):
                    # 判断并记录发送时间靠前的弹幕索引
                    if (group.iloc[i]['timestamp'] < group.iloc[j]['timestamp']):
                        j = i
                    index_to_drop.append(group.iloc[j].name)
    # 删除记录在列表的弹幕后写入csv
    tmp_dm = tmp_dm.drop(index_to_drop)
    tmp_dm.to_csv(danmu_output_path)


# 计算视频各个时间段弹幕数量并输出为csv
# 输入弹幕文件路径以及划分时间段的长度
def danmu_counts(danmu_csv_path, block_length, time_list_output_path):
    # 读取弹幕文件
    tmp_dm = pd.read_csv(danmu_csv_path)
    # 确定时间区间总分组数量和所选区间数量
    block_number = (((max(tmp_dm['elapse_time']) / block_length) + 1).__round__())  # 总数量
    block2chose = (((max(tmp_dm['elapse_time']) / (block_length*10)) + 1).__round__())  # 所选数量
    # bins储存需要统计的时间时间划分
    bins = []
    for i in range(0, block_number):
        bins.append(block_length * i)  # 代表block_length秒划分一段区间
    # 开始按区间统计数据数量
    cuts = pd.cut(tmp_dm['elapse_time'], bins)
    counts = pd.value_counts(cuts)
    # 初始化储存信息的列表
    block_list = pd.DataFrame()
    start_time = []
    end_time = []
    danmu_number = []
    block_counts = 0
    # 通过for循环记录每个区间弹幕的数量
    for key, value in dict(counts).items():
        # 只记录前10%的时间段
        if block_counts <= block2chose:
            block_counts = block_counts + 1
            start_time.append(int(key.left))
            end_time.append(int(key.right))
            danmu_number.append(int(value))
    #
    block_list['start'] = start_time
    block_list['end'] = end_time
    block_list['counts'] = danmu_number
    block_list = block_list.sort_values(by='start')
    block_list.to_csv(time_list_output_path)

    # 重新初始化利用,以记录切割时间分割
    start_time = []
    end_time = []
    # 迭代往前循环,并合并时间相邻的和时间只相差一个时间段的
    before = -1
    for now in block_list['start']:
        if before == -1:
            start_time.append(now)
            before = now
            continue
        if (now - block_length) == before or (now - 2*block_length) == before:
            before = now
            continue
        start_time.append(now)
        end_time.append(before + block_length)
        before = now
    # 最后一个片段没有截止时间则去除
    if len(start_time) > len(end_time):
        start_time = start_time[:-1]
    time_list = pd.DataFrame()
    time_list['start'] = start_time
    time_list['end'] = end_time
    # 删除单独的时间段片段
    time_list = time_list.drop(time_list[(time_list.end - time_list.start == block_length)].index)
    time_list = time_list.set_index('start')
    time_list.to_csv('highlight_block.csv')


if __name__ == "__main__":
    # 输入视频链接
    # video_url = input('请输入视频链接\n')
    # # 通过视频链接获取弹幕数据
    # get_dm_to_csv(cid_to_url(url_get_cid(video_url)), 'B站弹幕.csv')
    # # 进行以同用户发言相似度为基准的预处理
    # clear_similarities('B站弹幕.csv', 'B站弹幕2.csv')
    # # 对时间的区间弹幕数量统计
    danmu_counts('ba wang bie ji 2.csv.csv', 4, 'video_time_list.csv')

    # plt.hist(dm_time, bins=int(max(dm_time) / 3))  # bins表示将数据分为多少个区间,与视频时间相关
    # plt.title('Barrage Histogram')
    # plt.xlabel('Time')
    # plt.ylabel('Barrage Count')
    # plt.show()
