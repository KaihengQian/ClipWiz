from hyperopt import hp, fmin, rand
import danmu_other_helper_functions
import danmu_evaluation_functions
import danmu_counts_helper_functions
import danmu_emotion_helper_functions

# 创建文件夹
home_folder_path = r"D:\双创"  # 主文件路径
subfolder_name = "sample_1"  # 子文件夹名称
subfolder_path = danmu_other_helper_functions.create_subfolder(home_folder_path, subfolder_name)

block_info_path = subfolder_path + r"\result\danmu_block_info.csv"
time_list_path = subfolder_path + r"\result\time_list.csv"
evaluation_path = subfolder_path + r"\result\evaluation.txt"
predict_data_path = subfolder_path + r"\result\predict_data.csv"
danmu_path = subfolder_path + r"\result\danmu.csv"
selected_danmu_path = subfolder_path + r"\result\selected_danmu.csv"


def q(args):
    chose_rate_1, move_time = args
    result = 0

    for i in range(1, 11):
        stamp_data_path = r"D:\双创\highlights\vedio_" + str(i) + ".csv"
        origin_danmu_path = r"D:\双创\time_order\vedio_" + str(i) + ".csv"
        # 减去发送弹幕误差时间(路径,前推秒数)
        danmu_counts_helper_functions.elapse_time_move(origin_danmu_path, danmu_path, move_time)

        # 对时间的区间弹幕数量统计(弹幕路径,分区时间长度,输出时间表路径,选择比例)
        danmu_counts_helper_functions.danmu_counts(danmu_path, 3, time_list_path, chose_rate_1)

        # 选择需要后续情感分析处理的弹幕
        danmu_counts_helper_functions.select_danmu(time_list_path, danmu_path, selected_danmu_path)

        # 对所选时间片段内的弹幕以情感值选取比例(所选弹幕csv,时间分区长度,基于原视频总长度的选择比例)
        danmu_emotion_helper_functions.emotion_count(selected_danmu_path, 3, 0.2, time_list_path)

        # 应用评估函数对准确率进行评价
        result += danmu_evaluation_functions.evaluation_function(time_list_path, stamp_data_path, evaluation_path, predict_data_path)

    return -result


space = [hp.uniform('chose_rate_1', 0.2, 0.6),
         hp.uniform('move_time', 0, 3)]
best = fmin(q, space, algo=rand.suggest, max_evals=100)
print(best)

# 4秒,情感绝对值求和策略
# 3秒,情感绝对值求和策略  {'chose_rate_1': 0.29979346553473035, 'move_time': 2.9325352642770355}
# 5秒,情感绝对值求和策略