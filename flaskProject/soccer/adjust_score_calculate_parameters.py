from hyperopt import hp, fmin, rand
import soccer_other_helper_functions
import soccer_evaluation_functions


user_name = "user1439"
video_name = "soccer1"
list_name = "timelist1"

subfolder_path = r"D:\Code\Project\User\soccer_User\User_1439"
input_video_path = subfolder_path + r"\data\video.mp4"
event_path = r"F:\双创\soccer\dataset\event\1439_event.txt"
story_path = r"F:\双创\soccer\dataset\event\1439_story.txt"
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

# 1400： {'w_1': 0.3533101321614365, 'w_2': 0.04126411495198157, 'w_3': 0.7999121629831752}
# 1404： {'w_1': 0.4114122588334779, 'w_2': 0.9071399484280444, 'w_3': 0.04430738475460905}
# 1409： {'w_1': 0.04807045027117385, 'w_2': 0.7837087341315977, 'w_3': 0.17318603960332712}
# 1434： {'w_1': 0.2766793425173443, 'w_2': 0.007089828399028386, 'w_3': 0.6455573525907463}
# 1435： {'w_1': 0.35252364474571907, 'w_2': 0.008243960259199046, 'w_3': 0.760203845130488}
# 1436： {'w_1': 0.09353559696114988, 'w_2': 0.6067208191891683, 'w_3': 0.6815754859207594}
# 1437： {'w_1': 0.6514528563119463, 'w_2': 0.9976447591332872, 'w_3': 0.6544367891478955}
# 1438： {'w_1': 0.5530021224963927, 'w_2': 0.868947925313886, 'w_3': 0.19111335502874616}
# 1439： {'w_1': 0.21804618951548238, 'w_2': 0.548746099051057, 'w_3': 0.30544524723847655}
# 1440： {'w_1': 0.6019486526206175, 'w_2': 0.28253425741242055, 'w_3': 0.1526505411088095}
# 1441： {'w_1': 0.8925507456984548, 'w_2': 0.10007669795808216, 'w_3': 0.22112031726510006}
# 1442： {'w_1': 0.5671763600545594, 'w_2': 0.4290359177953762, 'w_3': 0.007899758045850525}
# 1443： {'w_1': 0.538921636239424, 'w_2': 0.6537644800638118, 'w_3': 0.20199007444818706}
# 1444： {'w_1': 0.8721624108210301, 'w_2': 0.29366967422812995, 'w_3': 0.03899471938280863}
# 1445： {'w_1': 0.011703183253705673, 'w_2': 0.15069287453108682, 'w_3': 0.412981811383074}
# 1446： {'w_1': 0.15960260907760282, 'w_2': 0.08238888621551754, 'w_3': 0.7592335434736031}
# 1447： {'w_1': 0.4058033706490667, 'w_2': 0.05875956857009723, 'w_3': 0.6453912838696575}
# 1448： {'w_1': 0.3937278703903585, 'w_2': 0.868770984470414, 'w_3': 0.6092057792177344}
# 1449： {'w_1': 0.5260560697686519, 'w_2': 0.9829109570470614, 'w_3': 0.916403724258741}
