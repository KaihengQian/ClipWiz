import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
# import matplotlib.pyplot as plt
import jieba
from sqlalchemy import create_engine, text
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/user1')

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
def get_dm_to_csv(dm_url):
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
    # dm.to_csv(danmu_output_path, index=False)
    # 写入数据库
    dm.to_sql('record', con=engine, if_exists='replace', index=False)
    print("弹幕导入成功")
    # # 输出弹幕数量,以作分析
    # print('弹幕数量为')
    # print(len(dm))
    # 清空列表存储内容
    dm_time.clear()
    dm_text.clear()
    dm_user.clear()
    dm_date.clear()


def elapse_time_move(move_time):
    tmp_dm = pd.read_sql(text("select * from record"), engine.connect())
    tmp_dm = tmp_dm.sort_values(by='elapse_time')
    new_elapse_time = []
    # 依次减少时间,最后一个最大时间作为视频时长依据保持不变
    for i in range(0, len(tmp_dm)-1):
        if(tmp_dm.iloc[i]['elapse_time'] < move_time):
            new_elapse_time.append(tmp_dm.iloc[i]['elapse_time'])
            continue
        new_elapse_time.append(tmp_dm.iloc[i]['elapse_time']-move_time)
    new_elapse_time.append(max(tmp_dm['elapse_time']))
    # 写入csv
    tmp_dm['elapse_time'] = new_elapse_time
    tmp_dm.to_sql('tmp', con=engine, if_exists='replace', index=False)
    print("时间误差补偿成功")


def clear_similarities():
    tmp_dm = pd.read_sql(text("select * from tmp"), engine.connect())
    group_dm = tmp_dm.groupby('user_id')
    index_to_drop = []
    # 循环处理每一个组
    for name, group in group_dm:
        group_size = len(group)
        # 只发送一个弹幕的不进行处理
        if group_size == 1:
            continue
        # 相同发送用户的弹幕间两两进行判定
        for i in range(group_size):
            for j in range(i + 1, group_size):
                # 判断弹幕相似度,以jaccard系数0.7为阈值
                if (jaccard(group.iloc[i]['text'], group.iloc[j]['text']) > 0.7):
                    # 判断并记录发送时间靠前的弹幕索引
                    if (group.iloc[i]['timestamp'] < group.iloc[j]['timestamp']):
                        j = i
                    index_to_drop.append(group.iloc[j].name)
    # 删除记录在列表的弹幕后写入数据库
    tmp_dm = tmp_dm.drop(index_to_drop)
    # tmp_dm.to_csv(danmu_output_path, index=False)
    tmp_dm.to_sql('denoise', con=engine, if_exists='replace', index=False)
    print("去噪成功")


def danmu_counts(block_length, chose_rate):

    # 读取弹幕文件
    tmp_dm = pd.read_sql(text("select * from denoise"), engine.connect())
    # 确定时间区间总分组数量和所选区间数量
    video_length = max(tmp_dm['elapse_time'])
    block_number = (((video_length / block_length) + 1).__round__())  # 总数量
    block2chose = int(block_number * chose_rate)  # 所选数量
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
        # 只记录部分的时间段
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
    # block_list.to_csv(time_list_output_path, index=False)

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
        end_time.append(video_length)
    time_list = pd.DataFrame()
    time_list['start'] = start_time
    time_list['end'] = end_time
    # 删除单独的时间段片段
    time_list = time_list.drop(time_list[(time_list.end - time_list.start == block_length)].index)
    time_list.to_sql('time_list', con=engine, if_exists='replace', index=False)
    print("时间初筛成功")


def select_danmu():
    # 初始化需选择的弹幕时间列表界限和去除列表
    upper_bound = []
    lower_bound = []
    # 读取弹幕和时间
    origin_danmu = pd.read_sql(text("select elapse_time,text from denoise"), engine.connect())
    origin_danmu['elapse_time'] = origin_danmu['elapse_time'].astype(int)
    time_list = pd.read_sql(text("select * from time_list"), engine.connect())
    # 获取时间范围
    list_length = len(time_list)
    for i in range(0, list_length):
        lower_bound.append(int(time_list.iloc[i]['start']))
        upper_bound.append(int(time_list.iloc[i]['end']))
    time_range = pd.DataFrame({
        'start': lower_bound,
        'end': upper_bound
    })
    mask = time_range.apply(lambda row: (row['start'] <= origin_danmu['elapse_time']) & (origin_danmu['elapse_time'] <= row['end']), axis=1)
    selected_danmu = origin_danmu.loc[mask.any(axis=0)]
    selected_danmu = selected_danmu.sort_values(by='elapse_time')
    # selected_danmu.to_csv(danmu_output_path, index=False)
    selected_danmu.to_sql('selected_danmu', con=engine, if_exists='replace', index=False)
    print("弹幕初筛成功")


# 展示弹幕数据图
# def show_danmu_plt(danmu_input_path, fig_path):
#     dm = pd.read_csv(danmu_input_path)
#     dm_time = dm['elapse_time']
#     plt.hist(dm_time, bins=int(max(dm_time) / 3))  # bins表示将数据分为多少个区间,与视频时间相关
#     plt.title('Barrage Histogram')
#     plt.xlabel('Time')
#     plt.ylabel('Barrage Count')
#     plt.savefig(fig_path)




