import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from moviepy.editor import AudioFileClip
import librosa.display


def audio_extract(video_path, audio_path):
    my_audio_clip = AudioFileClip(video_path)
    my_audio_clip.write_audiofile(audio_path)  # 保存音频格式为.wav


def audio_pre_emphasis(audio):
    u = 0.9375  # 设置预加重系数
    for i in range(1, int(len(audio))):
        audio[i] = audio[i] - u * audio[i-1]  # 一阶高通滤波器
    return audio


def audio_energy(audio, sample_rate, sample_number, block_number, block_audio_info_path):
    block_audio_info = pd.read_csv(block_audio_info_path)

    # graph_1_path = "E:\\双创\\soccer\\result\\audio_wave.png"  # 音频波形图
    # plt.figure(figsize=(20, 5))
    # librosa.display.waveshow(audio, sr=sample_rate)
    # plt.savefig(graph_1_path)

    # 计算每个块的短时能量，即求时域中音频信号幅度的平方和
    energy = np.array([sum(abs(audio[i * sample_number:(i + 1) * sample_number] ** 2)) for i in range(block_number)])
    # graph_2_path = "E:\\双创\\soccer\\result\\audio_short-time_energy_distribution.png"  # 短时能量分布图
    # plt.hist(energy)
    # plt.savefig(graph_2_path)
    processed_energy = (energy - np.min(energy)) / (np.max(energy) - np.min(energy))
    block_audio_info['energy'] = processed_energy

    block_audio_info.to_csv(block_audio_info_path, index=False)


def audio_zero_crossings(audio, sample_rate, sample_number, block_number, block_audio_info_path):
    block_audio_info = pd.read_csv(block_audio_info_path)

    # graph_3_path = "E:\\双创\\soccer\\result\\audio_zero_crossing_rate.png"  # 过零率图
    # zero_crossing_rate = librosa.feature.zero_crossing_rate(audio + 0.0001)
    # zero_crossing_rate_times = librosa.frames_to_time(np.arange(len(zero_crossing_rate[0])), sr=sample_rate,
    # hop_length=512)  # 将横轴信息由帧转化为时间
    # plt.figure(figsize=(14, 5))
    # plt.plot(zero_crossing_rate_times, zero_crossing_rate[0])
    # plt.savefig(graph_3_path)

    zero_crossings = []
    for i in range(block_number):
        temp = librosa.zero_crossings(audio[i * sample_number:(i + 1) * sample_number] + 0.0001, pad=False)
        # 音频最开始的“无声”区域中有许多小数值的样本分布在界限0的两侧，计算得到的过零率会过高，解决方法是给整个音频样本的数值都加个极小的常数
        zero_crossings.append(temp.sum())
    zero_crossings = np.array(zero_crossings)
    # graph_4_path = "E:\\双创\\soccer\\result\\audio_zero_crossings.png"  # 过零次数图
    # plt.hist(energy)
    # plt.savefig(graph_4_path)
    processed_zero_crossings = (zero_crossings - np.min(zero_crossings)) / (np.max(zero_crossings) -
                                                                            np.min(zero_crossings))
    block_audio_info['zero_crossings'] = processed_zero_crossings

    block_audio_info.to_csv(block_audio_info_path, index=False)
