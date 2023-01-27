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



