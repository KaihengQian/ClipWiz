from hyperopt import hp, fmin, rand
import soccer_other_helper_functions
import soccer_evaluation_functions


user_name = "user1448"
video_name = "soccer1"
list_name = "timelist1"

subfolder_path = r"D:\Code\Project\User\soccer_User\User_1448"
input_video_path = subfolder_path + r"\data\video.mp4"
event_path = r"E:\双创\soccer\dataset\event\1448_event.txt"
story_path = r"E:\双创\soccer\dataset\event\1448_story.txt"
predict_event_path = subfolder_path + r"\result\predict_event_1.csv"
predict_story_path = subfolder_path + r"\result\predict_story_1.csv"
evaluation_path = subfolder_path + r"\result\evaluation_1.txt"

database = soccer_other_helper_functions.connect_database(user_name, video_name, list_name)

def q(args):
    w_1, w_2, w_3 = args
    # 计算块的最终得分
    soccer_other_helper_functions.score_calculate(w_1, w_2, w_3, database, video_name)

    # 获取所需块的时间序列
    soccer_other_helper_functions.get_time_list(database, video_name, list_name)

    # 应用评估函数对准确率进行评价
    result = soccer_evaluation_functions.evaluation_function(input_video_path, database, list_name, event_path,
                                            story_path, predict_event_path, predict_story_path, evaluation_path)

    return -result


space = [hp.uniform('w_1', 0, 1), hp.uniform('w_2', 0, 1), hp.uniform('w_3', 0, 1)]
best = fmin(q, space, algo=rand.suggest, max_evals=1000)
print(best)

database.close()

# 1448： {'w_1': 0.3937278703903585, 'w_2': 0.868770984470414, 'w_3': 0.6092057792177344}
# 1449： {'w_1': 0.9455894941737084, 'w_2': 0.307730170204933}
