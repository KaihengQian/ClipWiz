import os
import shutil
import numpy as np
import pandas as pd
import math
from moviepy import editor


def create_subfolder(home_folder_path, subfolder_name):
    subfolder_path = home_folder_path + "./" + subfolder_name
    if os.path.exists(subfolder_path):  # 检测要创建的子文件夹是否已经存在
        print("The folder already exists.")
        shutil.rmtree(subfolder_path)  # 删除已经存在的子文件夹
    os.mkdir(subfolder_path)
    subfolder_path = os.path.join(home_folder_path, "./" + subfolder_name)
    file_name = ["./data", "./result", "./graph"]
    for name in file_name:
        os.mkdir(subfolder_path + name)
    return subfolder_path


def score_calculate(block_audio_info_path):
    weight_1 = 0.3263118490343915
    weight_2 = 0.49079651798722146
    block_audio_info = pd.read_csv(block_audio_info_path)
    block_audio_info['score'] = block_audio_info['energy'] * weight_1 + block_audio_info['zero_crossings'] * weight_2
    block_audio_info.to_csv(block_audio_info_path, index=False)


def get_time_list(block_audio_info_path, time_list_path):
    block_audio_info = pd.read_csv(block_audio_info_path)
    time_list = pd.DataFrame(columns=['start', 'end'])

    # 根据得分筛选得到所需块
    score = np.array(block_audio_info['score'])
    score.sort()
    threshold_rate = 0.96  # 设置阈值以筛选得分最高的4%的块
    threshold = score[math.ceil(threshold_rate * len(score))]
    time_list.loc[0, 'start'] = block_audio_info.loc[0, 'start']  # 第一个块必定选择
    time_list.loc[0, 'end'] = block_audio_info.loc[0, 'end']
    row_index = 1
    for i in range(len(block_audio_info)):
        if block_audio_info.loc[i, 'score'] >= threshold:
            time_list.loc[row_index, 'start'] = block_audio_info.loc[i, 'start']
            time_list.loc[row_index, 'end'] = block_audio_info.loc[i, 'end']
            row_index += 1

    # 合并时间相邻的块，更新时间序列
    temp = []
    i = 0
    j = 0
    m = len(time_list) - 2
    n = len(time_list) - 1
    while i <= m:
        j = i + 1
        while j <= n:
            if time_list.loc[i, 'end'] == time_list.loc[j, 'start']:
                time_list.loc[i, 'end'] = time_list.loc[j, 'end']
                temp.append(j)
                j += 1
            else:
                i = j
                break
    time_list.drop(temp, inplace=True)
    time_list.reset_index(drop=True)

    # 考虑反应时间，将块的开始时间相应提前
    response_time = 5
    for i in range(len(time_list)):
        if time_list.iloc[i]['start'] >= response_time:
            time_list.iloc[i]['start'] -= response_time

    time_list.to_csv(time_list_path, index=False)


def video_edit(input_video_path, time_list_path, output_video_path):
    video_input = editor.VideoFileClip(input_video_path)

    time_list = pd.read_csv(time_list_path)
    start_list = np.array(time_list['start'])
    end_list = np.array(time_list['end'])

    start = start_list[0]
    end = end_list[0]
    video_output = video_input.subclip(start, end)
    for i in range(1, len(start_list)):
        start = start_list[i]
        end = end_list[i]
        temp = video_input.subclip(start, end)
        video_output = editor.concatenate_videoclips([video_output, temp])

    video_output.write_videofile(output_video_path)

