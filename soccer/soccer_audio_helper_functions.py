import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from moviepy.editor import AudioFileClip


def audio_extract(video_path, save_path):
    my_audio_clip = AudioFileClip(video_path)
    my_audio_clip.write_audiofile(save_path)  # 保存音频格式为.wav


def audio_energy(audio, sample_number, block_number, block_audio_info_path):
    block_audio_info = pd.read_csv(block_audio_info_path)

    energy = np.array([sum(abs(audio[i * sample_number:(i + 1) * sample_number] ** 2)) for i in
                       range(block_number)])  # 计算每个块的短时能量，即求时域中音频信号幅度的平方和
    # graph_path = "C:\\Users\\user\\Desktop\\本科\\双创\\代码\\result\\soccer_short-time_energy_distribution.png"
    # plt.hist(energy)
    # plt.savefig(graph_path)
    for i in range(len(energy)):
        block_audio_info.loc[i, 'start'] = i * 5
        block_audio_info.loc[i, 'end'] = (i + 1) * 5
        block_audio_info.loc[i, 'energy'] = energy[i]

    block_audio_info.to_csv(block_audio_info_path)


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

    # 将每个块的开始时间提早5秒
    for i in range(len(time_list)):
        if time_list.loc[i, 'start'] >= 5:
            time_list.loc[i, 'start'] -= 5

    time_list.to_csv(time_list_path)

