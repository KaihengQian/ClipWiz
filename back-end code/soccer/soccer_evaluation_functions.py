import numpy as np
import pandas as pd
import cv2


def evaluation_function(input_video_path, time_list_path, event_path, story_path, predict_event_path,
                        predict_story_path, evaluation_path):
    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(5)  # 获取帧率
    cap.release()

    # 转成以帧为单位
    time_list = pd.read_csv(time_list_path)
    our_start = np.array(time_list['start']) * fps
    our_end = np.array(time_list['end']) * fps

    # 以空格为分隔符读取event和story，并添加字段名
    event = pd.read_csv(event_path, delim_whitespace=True, header=None, names=['event_type', 'start_point', 'end_point',
                                                                               'flag'])
    event_start = np.array(event['start_point'])
    event_end = np.array(event['end_point'])
    story = pd.read_csv(story_path, delim_whitespace=True, header=None, names=['story_type', 'start_point',
                                                                               'end_point'])
    story_start = np.array(story['start_point'])
    story_end = np.array(story['end_point'])

    predict_event = event
    predict_event['weight'] = 0  # 为不同事件赋不同权重
    predict_event.loc[
        (((predict_event['event_type'] == 'overhead-kick') | (predict_event['event_type'] == 'solo-drive') |
         (predict_event['event_type'] == 'goal') | (predict_event['event_type'] == 'penalty-kick') |
         (predict_event['event_type'] == 'red-card')) & (predict_event['flag'] == 0)), 'weight'] = 3
    predict_event.loc[
        (((predict_event['event_type'] == 'overhead-kick') | (predict_event['event_type'] == 'solo-drive') |
         (predict_event['event_type'] == 'goal') | (predict_event['event_type'] == 'penalty-kick') |
         (predict_event['event_type'] == 'red-card')) & (predict_event['flag'] == 1)), 'weight'] = 2
    predict_event.loc[((predict_event['event_type'] == 'shot') & (predict_event['flag'] == 0)), 'weight'] = 1
    predict_event_result = np.zeros(len(event_start))  # 保存预测结果与标注的交集
    i = 0
    j = 0
    while i < len(our_start) and j < len(event_start):
        if our_start[i] >= event_end[j]:
            j += 1
        elif our_end[i] <= event_start[j]:
            i += 1
        else:
            intersection_start = max(our_start[i], event_start[j])
            intersection_end = min(our_end[i], event_end[j])
            intersection = intersection_end - intersection_start
            predict_event_result[j] += intersection
            if our_end[i] < event_end[j]:
                i += 1
            else:
                j += 1

    predict_event['predict_result'] = predict_event_result
    predict_event['score'] = predict_event['predict_result'] / (predict_event['end_point'] -
                                                                predict_event['start_point']) * predict_event['weight']
    predict_event.to_csv(predict_event_path, index=False)

    predict_story = story
    predict_story['weight'] = 0  # 为不同事件赋不同权重
    predict_story.loc[
        ((predict_story['story_type'] == 'overhead-kick') | (predict_story['story_type'] == 'solo-drive') |
         (predict_story['story_type'] == 'goal') | (predict_story['story_type'] == 'penalty-kick') |
         (predict_story['story_type'] == 'red card') | (predict_story['story_type'] == 'corner & goal') |
         (predict_story['story_type'] == 'free-kick & goal')), 'weight'] = 3
    predict_story.loc[((predict_story['story_type'] == 'corner & shot') |
                      (predict_story['story_type'] == 'free-kick & shot')), 'weight'] = 2
    predict_story.loc[(predict_story['story_type'] == 'shot'), 'weight'] = 1
    predict_story_result = np.zeros(len(story_start))  # 保存预测结果与标注的交集
    i = 0
    j = 0
    while i < len(our_start) and j < len(story_start):
        if our_start[i] >= story_end[j]:
            j += 1
        elif our_end[i] <= story_start[j]:
            i += 1
        else:
            intersection_start = max(our_start[i], story_start[j])
            intersection_end = min(our_end[i], story_end[j])
            intersection = intersection_end - intersection_start
            predict_story_result[j] += intersection
            if our_end[i] < story_end[j]:
                i += 1
            else:
                j += 1

    predict_story['predict_result'] = predict_story_result
    predict_story['predict_result_percentage'] = predict_story['predict_result'] / (
                predict_story['end_point'] - predict_story['start_point'])
    predict_story['score'] = predict_story['predict_result_percentage'] * predict_story['weight']
    predict_story.to_csv(predict_story_path, index=False)

    # 计算加权召回率
    event_weight = np.array(predict_event['weight'])
    event_weight = event_weight.sum()
    predict_event_score = np.array(predict_event['score'])
    predict_event_score = predict_event_score.sum()
    predict_event_recall_rate = float(format(predict_event_score / event_weight * 100, '.2f'))

    story_weight = np.array(predict_story['weight'])
    story_weight = story_weight.sum()
    predict_story_score = np.array(predict_story['score'])
    predict_story_score = predict_story_score.sum()
    predict_story_recall_rate = float(format(predict_story_score / story_weight * 100, '.2f'))

    # 计算精确率
    predict_time_sum = (our_end - our_start).sum()

    predict_event_result = predict_event_result.sum()
    predict_event_precision_rate = float(format(predict_event_result / predict_time_sum * 100, '.2f'))

    predict_story_result = predict_story_result.sum()
    predict_story_precision_rate = float(format(predict_story_result / predict_time_sum * 100, '.2f'))

    # 计算F_beta值
    predict_event_F_beta = 2 * predict_event_precision_rate * predict_event_recall_rate / ((predict_event_precision_rate
                                                                                            + predict_event_recall_rate) * 100)
    predict_story_F_beta = 2 * predict_story_precision_rate * predict_story_recall_rate / ((predict_story_precision_rate
                                                                                            + predict_story_recall_rate) * 100)

    # 输出评价结果
    evaluation = "针对event的加权召回率为：  " + str(predict_event_recall_rate) + "%\n" + \
                 "针对event的精确率为：  " + str(predict_event_precision_rate) + "%\n" + \
                 "针对event的F_beta值为：  " + str(predict_event_F_beta) + "\n" + \
                 "针对story的加权召回率为：  " + str(predict_story_recall_rate) + "%\n" + \
                 "针对story的精确率为：  " + str(predict_story_precision_rate) + "%\n" + \
                 "针对story的F_beta值为：  " + str(predict_story_F_beta)
    with open(evaluation_path, "w") as f:
        f.write(evaluation)

    return (predict_event_F_beta + predict_story_F_beta) / 2
