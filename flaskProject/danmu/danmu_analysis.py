import os
import danmu_counts_helper_functions
import danmu_emotion_helper_functions
import danmu_other_helper_functions
import danmu_evaluation_functions
import danmu_highlights_play
import time

# from sqlalchemy import create_engine, text
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/danmu')

# 创建文件夹
# home_folder_path = r"D:\双创"  # 主文件路径
# subfolder_name = "sample_1"  # 子文件夹名称
# subfolder_path = danmu_other_helper_functions.create_subfolder(home_folder_path, subfolder_name)

# 保存路径
# danmu_path = subfolder_path + r"\result\danmu.csv"
# selected_danmu_path = subfolder_path + r"\result\selected_danmu.csv"
# block_info_path = subfolder_path + r"\result\danmu_block_info.csv"
# time_list_path = subfolder_path + r"\result\time_list.csv"
# evaluation_path = subfolder_path + r"\result\evaluation.txt"
# barrage_histogram_path = subfolder_path + r"\graph\barrage_histogram.jpg"
# predict_data_path = subfolder_path + r"\result\predict_data.csv"

# stamp_data_path = r"D:\双创\reference_summary\vedio_8.csv"
# origin_danmu_path = r"D:\双创\time_order\vedio_8.csv"

# 输入视频链接
video_url = input('请输入视频链接：\n')

# 通过视频链接获取弹幕数据
danmu_counts_helper_functions.get_dm_to_csv(danmu_counts_helper_functions.cid_to_url(danmu_counts_helper_functions.bv_get_cid(video_url)))

# 依据弹幕数量做图
# danmu_counts_helper_functions.show_danmu_plt(danmu_path, barrage_histogram_path)

# 减去发送弹幕误差时间(路径,前推秒数)
danmu_counts_helper_functions.elapse_time_move(2.9744177916212657)

# 进行以同用户发言相似度为基准的预处理
danmu_counts_helper_functions.clear_similarities()

# 对时间的区间弹幕数量统计(弹幕路径,分区时间长度,输出时间表路径,选择比例)
danmu_counts_helper_functions.danmu_counts(3, 0.2870985733500858)

# 选择需要后续情感分析处理的弹幕
danmu_counts_helper_functions.select_danmu()

# 为所选弹幕进行情感分析赋值
danmu_emotion_helper_functions.text_score()

# 对所选时间片段内的弹幕以情感值选取比例(所选弹幕csv,时间分区长度,基于原视频总长度的选择比例)
danmu_emotion_helper_functions.emotion_count(3, 0.15)


# 应用评估函数对准确率进行评价
# danmu_evaluation_functions.evaluation_function(time_list_path, stamp_data_path, evaluation_path, predict_data_path)

# 播放集锦
# danmu_highlights_play.highlights_play(time_list_path, video_url)

# 删除弹幕
# os.remove(danmu_path)