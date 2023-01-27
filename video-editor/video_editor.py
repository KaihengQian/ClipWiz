import numpy as np
import pandas as pd
import math
from moviepy import editor


def get_time_list(block_audio_info_path, time_list_path):
    block_audio_info = pd.read_csv(block_audio_info_path)
    time_list = pd.DataFrame(columns=['start', 'end'])

    # 根据得分筛选得到所需块
    score = np.array(block_audio_info['score'])
    score.sort()
    threshold_rate = 0.96  # 设置阈值以筛选得分最高的4%的块
    threshold = score[math.ceil(threshold_rate * len(score))]
    row_index = 0
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
        if time_list.loc[i, 'start'] >= response_time:
            time_list.loc[i, 'start'] -= response_time

    time_list.to_csv(time_list_path)


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

