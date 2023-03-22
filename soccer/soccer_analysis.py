import os
import math
import pandas as pd
import librosa
import webbrowser
import soccer_other_helper_functions
import soccer_audio_helper_functions
import soccer_cv_helper_functions
import soccer_evaluation_function
import time


time_spent = []

# 创建文件夹
# home_folder_path = r"D:\Code\Project\User"  # 主文件路径
# subfolder_name = "User_2"  # 子文件夹名称
# subfolder_path = soccer_other_helper_functions.create_subfolder(home_folder_path, subfolder_name)
subfolder_path = r"D:\Code\Project\User\User_3"

# 保存路径
# raw_video_path = r"E:\双创\soccer\dataset\video\soccer_0001_video.mp4"
input_video_path = subfolder_path + r"\data\video.mp4"
audio_path = subfolder_path + r"\data\audio.wav"
block_audio_info_path = subfolder_path + r"\result\soccer_block_audio_info.csv"
time_list_path = subfolder_path + r"\result\time_list.csv"
output_video_path = subfolder_path + r"\result\highlights.mp4"
event_path = r"E:\双创\soccer\dataset\event\1448_event.txt"
story_path = r"E:\双创\soccer\dataset\event\1448_story.txt"
predict_event_path = subfolder_path + r"\result\predict_event.csv"
predict_story_path = subfolder_path + r"\result\predict_story.csv"
evaluation_path = subfolder_path + r"\result\evaluation.txt"
html_file_path = r"D:\Code\Project\front-end code\soccer\soccer_highlights_play.html"


# 视频预处理（剪切去除开球前的视频片段）
# soccer_cv_helper_functions.video_preprocess(raw_video_path, input_video_path)

t1 = time.perf_counter()
# 提取音频
soccer_audio_helper_functions.audio_extract(input_video_path, audio_path)

# 音频预处理
audio, sample_rate = librosa.load(audio_path, sr=24000)  # 加载音频，设置采样率
audio = soccer_audio_helper_functions.audio_pre_emphasis(audio)  # 音频预加重
time_slice = 5  # 将音频划分为时长均为5秒的块
sample_number = time_slice * sample_rate  # 计算每一块的采样数（采样数=采样率*采样时间）
block_number = math.ceil(len(audio) / sample_number)  # 计算块数量
t2 = time.perf_counter()
time_spent.append(t2 - t1)

# 用于保存每个块的详细信息
column_names = ['start', 'end', 'energy', 'zero_crossings', 'score']
block_audio_info = pd.DataFrame(columns=column_names)

# 获取块的开始时间、结束时间信息
for i in range(block_number):
    block_audio_info.loc[i, 'start'] = i * 5
    block_audio_info.loc[i, 'end'] = (i + 1) * 5
block_audio_info.to_csv(block_audio_info_path, index=False)

# 获取块的能量信息
soccer_audio_helper_functions.audio_energy(audio, sample_rate, sample_number, block_number, block_audio_info_path)

# 获取块的过零率信息
soccer_audio_helper_functions.audio_zero_crossings(audio, sample_rate, sample_number, block_number,
                                                   block_audio_info_path)

# 删除音频文件
os.remove(audio_path)

# 计算块的最终得分
soccer_other_helper_functions.score_calculate(block_audio_info_path)

# 获取所需块的时间序列
soccer_other_helper_functions.get_time_list(block_audio_info_path, time_list_path)

t1 = time.perf_counter()
# 剪辑原视频获得集锦
soccer_other_helper_functions.video_edit(input_video_path, time_list_path, output_video_path)
t2 = time.perf_counter()
time_spent.append(t2 - t1)

# 应用评估函数对准确率进行评价
soccer_evaluation_function.evaluation_function(input_video_path, time_list_path, event_path, story_path,
                                               predict_event_path, predict_story_path, evaluation_path)

print(time_spent)

# 运行html文件播放集锦
webbrowser.open(html_file_path)
