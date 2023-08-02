import os
import danmu_counts_helper_functions
import danmu_emotion_helper_functions
import danmu_other_helper_functions
import danmu_evaluation_functions
import danmu_highlights_play


# 创建文件夹
home_folder_path = r"D:\Code\Project\User\danmu_User"  # 主文件路径
subfolder_name = "User_2"  # 子文件夹名称
subfolder_path = danmu_other_helper_functions.create_subfolder(home_folder_path, subfolder_name)

# 保存路径
danmu_path = subfolder_path + r"\result\danmu.csv"
selected_danmu_path = subfolder_path + r"\result\selected_danmu.csv"
block_info_path = subfolder_path + r"\result\danmu_block_info.csv"
time_list_path = subfolder_path + r"\result\time_list.csv"
evaluation_path = subfolder_path + r"\result\evaluation.txt"
predict_data_path = subfolder_path + r"\result\predict_data.csv"
barrage_histogram_path = subfolder_path + r"\graph\barrage_histogram.jpg"
stamp_data_path = r"E:\双创\danmu\dataset\highlights\ba wang bie ji.csv"

# 输入视频链接
video_url = input('请输入视频链接：\n')

# 通过视频链接获取弹幕数据
danmu_counts_helper_functions.get_dm_to_csv(danmu_counts_helper_functions.cid_to_url(danmu_counts_helper_functions.bv_get_cid(video_url)), danmu_path)

# 依据弹幕数量做图
danmu_counts_helper_functions.show_danmu_plt(danmu_path, barrage_histogram_path)

# 减去发送弹幕误差时间(路径,前推秒数)
danmu_counts_helper_functions.elapse_time_move(danmu_path, 1)

# 进行以同用户发言相似度为基准的预处理
danmu_counts_helper_functions.clear_similarities(danmu_path, danmu_path)

# 对时间的区间弹幕数量统计(弹幕路径,分区时间长度,输出时间表路径,选择比例)
danmu_counts_helper_functions.danmu_counts(danmu_path, 4, time_list_path, 0.5)

# 选择需要后续情感分析处理的弹幕
danmu_counts_helper_functions.select_danmu(time_list_path, danmu_path, selected_danmu_path)

# 为所选弹幕进行情感分析赋值
danmu_emotion_helper_functions.text_score(selected_danmu_path)

# 对所选时间片段内的弹幕情感分析(所选弹幕csv,时间分区长度,基于原视频总长度的选择比例)
danmu_emotion_helper_functions.emotion_count(selected_danmu_path, 4, 0.15, time_list_path)

# 应用评估函数对准确率进行评价
danmu_evaluation_functions.evaluation_function(time_list_path, stamp_data_path, evaluation_path, predict_data_path)

# 播放集锦
# danmu_highlights_play.highlights_play(time_list_path, video_url)

# 删除弹幕
# os.remove(danmu_path)
