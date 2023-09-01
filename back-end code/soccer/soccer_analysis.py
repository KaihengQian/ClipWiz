import math
import os

import librosa
import webbrowser
import soccer_other_helper_functions
import soccer_audio_helper_functions
import soccer_cv_helper_functions
import soccer_evaluation_functions
import time


# 用户名和视频类别及编号
user_name = "user1448"
video_name = "soccer1"
list_name = "timelist1"

# 创建文件夹
# home_folder_path = r"D:\Code\Project\User"  # 主文件路径
# subfolder_name = user_name + "/" + video_name  # 子文件夹名称
# subfolder_path = soccer_other_helper_functions.create_subfolder(home_folder_path, subfolder_name)
subfolder_path = r"D:\Code\Project\User\soccer_User\User_1448"

# 保存路径
raw_video_path = subfolder_path + r"\data\raw_video.mp4"
input_video_path = subfolder_path + r"\data\video.mp4"
audio_path = subfolder_path + r"\data\audio.wav"
output_video_path = subfolder_path + r"\result\highlights.mp4"
event_path = r"E:\双创\soccer\dataset\event\1448_event.txt"
story_path = r"E:\双创\soccer\dataset\event\1448_story.txt"
predict_event_path = subfolder_path + r"\result\predict_event.csv"
predict_story_path = subfolder_path + r"\result\predict_story.csv"
evaluation_path = subfolder_path + r"\result\evaluation.txt"
html_file_path = r"D:\Code\Project\front-end code\soccer\soccer_highlights_play.html"

weight_1 = 0.3937278703903585
weight_2 = 0.868770984470414
weight_3 = 0.6092057792177344

# 视频预处理（剪切去除开球前的视频片段）
soccer_cv_helper_functions.video_preprocess(raw_video_path, input_video_path)

t_1 = time.perf_counter()

# 提取音频
soccer_audio_helper_functions.audio_extract(input_video_path, audio_path)

# 音频预处理
duration = librosa.get_duration(filename=audio_path)
audio, sample_rate = librosa.load(audio_path, sr=24000)  # 加载音频，设置采样率
audio = soccer_audio_helper_functions.audio_pre_emphasis(audio, duration, sample_rate)  # 音频预加重
time_slice = 5  # 将音频划分为时长均为5秒的块
sample_number = time_slice * sample_rate  # 计算每一块的采样数（采样数=采样率*采样时间）
block_number = math.ceil(len(audio) / sample_number)  # 计算块数量

# 连接数据库
database = soccer_other_helper_functions.connect_database(user_name, video_name, list_name)

# 获取块的开始时间、结束时间信息
soccer_other_helper_functions.block_time(block_number, database, video_name)

# 获取块的能量信息
soccer_audio_helper_functions.audio_energy(audio, sample_rate, sample_number, block_number, database, video_name)

# 获取块的过零率信息
soccer_audio_helper_functions.audio_zero_crossings(audio, sample_rate, sample_number, block_number, database, video_name)

# 获取块的场景识别信息
soccer_cv_helper_functions.video_scene(input_video_path, database, video_name)

# 计算块的最终得分
soccer_other_helper_functions.score_calculate(weight_1, weight_2, weight_3, database, video_name)

# 获取所需块的时间序列
soccer_other_helper_functions.get_time_list(database, video_name, list_name)

# 剪辑原视频获得集锦
soccer_other_helper_functions.video_edit(input_video_path, database, list_name, output_video_path)

t_2 = time.perf_counter()
print("处理时间为" + str(t_2 - t_1) + "秒")

# 应用评估函数对准确率进行评价
# soccer_evaluation_functions.evaluation_function(input_video_path, database, list_name, event_path, story_path,
#                                                predict_event_path, predict_story_path, evaluation_path)

# 关闭数据库
database.close()

# 运行html文件播放集锦
# webbrowser.open(html_file_path)

# 删除音频文件
os.remove(audio_path)
