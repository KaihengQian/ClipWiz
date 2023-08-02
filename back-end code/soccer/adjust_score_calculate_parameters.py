from hyperopt import hp, fmin, rand
import soccer_other_helper_functions
import soccer_evaluation_functions


subfolder_path = r"D:\Code\Project\User\soccer_User\User_1449"

input_video_path = subfolder_path + r"\data\video.mp4"
block_audio_info_path = subfolder_path + r"\result\soccer_block_audio_info.csv"
time_list_path = subfolder_path + r"\result\time_list.csv"
event_path = r"E:\双创\soccer\dataset\event\1449_event.txt"
story_path = r"E:\双创\soccer\dataset\event\1449_story.txt"
predict_event_path = subfolder_path + r"\result\predict_event.csv"
predict_story_path = subfolder_path + r"\result\predict_story.csv"
evaluation_path = subfolder_path + r"\result\evaluation.txt"


def q(args):
    w_1, w_2 = args
    # 计算块的最终得分
    soccer_other_helper_functions.score_calculate(block_audio_info_path, w_1, w_2)

    # 获取所需块的时间序列
    soccer_other_helper_functions.get_time_list(block_audio_info_path, time_list_path)

    # 应用评估函数对准确率进行评价
    result = soccer_evaluation_functions.evaluation_function(input_video_path, time_list_path, event_path, story_path,
                                                             predict_event_path, predict_story_path, evaluation_path)

    return -result


space = [hp.uniform('w_1', 0, 1), hp.uniform('w_2', 0, 1)]
best = fmin(q, space, algo=rand.suggest, max_evals=1000)
print(best)

# 1448： {'w_1': 0.3263118490343915, 'w_2': 0.49079651798722146}
# 1449： {'w_1': 0.9455894941737084, 'w_2': 0.307730170204933}
