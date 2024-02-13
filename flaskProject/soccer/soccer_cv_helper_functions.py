import shutil
import numpy as np
import pymysql
import cv2
from moviepy import editor

import mobilenetv3.predict as pred


# 检测开球帧
def is_kick_off(frame):
    res = pred.predict(frame)
    return res == "start"


def video_preprocess(raw_video_path, input_video_path):
    cap = cv2.VideoCapture(raw_video_path)
    frame_num = cap.get(7)  # 获取总帧数
    fps = cap.get(5)  # 获取帧率
    time_interval = 0.5  # 设置检测间隔（单位为秒）
    frame_interval = int(fps * time_interval)  # 将检测间隔按单位换算为帧数
    c = 0  # 当前所在帧
    flag = 0  # 是否找到开球帧
    while c < (frame_num * 0.1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, c)
        ret, frame = cap.read()
        if ret:
            if is_kick_off(frame):
                time_interval = 0.25  # 缩小检测间隔
                frame_interval = int(fps * time_interval)
                c += frame_interval
                cap.set(cv2.CAP_PROP_POS_FRAMES, c)
                ret, frame = cap.read()
                while is_kick_off(frame):
                    c += frame_interval
                    cap.set(cv2.CAP_PROP_POS_FRAMES, c)
                    ret, frame = cap.read()
                c -= frame_interval
                flag = 1
                break
            c += frame_interval
            cv2.waitKey(0)
        else:
            break
    cap.release()

    start_frame = c
    start_time = start_frame / fps
    print(start_time)
    if flag and start_time >= 3:
        raw_video = editor.VideoFileClip(raw_video_path)
        video = raw_video.subclip(t_start=start_time)
        video.write_videofile(input_video_path)
    else:
        shutil.copy(raw_video_path, input_video_path)


def video_scene(video_path, db, table_name):
    # 各场景对应的得分
    penalty_score = 5
    red_card_score = 5
    joy_score = 4
    gate_score = 4
    free_kick_score = 3
    yellow_card_score = 2
    other_score = 1

    cap = cv2.VideoCapture(video_path)
    frame_num = cap.get(7)  # 获取总帧数
    fps = cap.get(5)  # 获取帧率
    time_interval = 1  # 设置检测间隔（单位为秒）
    frame_interval = int(fps * time_interval)  # 将检测间隔按单位换算为帧数
    c = 0  # 当前所在帧
    scene_score = []

    while c < frame_num:
        tmp_score = 0
        for i in range(5):
            cap.set(cv2.CAP_PROP_POS_FRAMES, c)
            ret, frame = cap.read()
            if ret:
                res = pred.predict(frame)
                if res == "penalty":
                    tmp_score += penalty_score
                elif res == "red_card":
                    tmp_score += red_card_score
                elif res == "joy":
                    tmp_score += joy_score
                elif res == "gate":
                    tmp_score += gate_score
                elif res == "free_kick":
                    tmp_score += free_kick_score
                elif res == "yellow_card":
                    tmp_score += yellow_card_score
                else:
                    tmp_score += other_score
                c += frame_interval
                cv2.waitKey(0)
            else:
                break
        scene_score.append(tmp_score)
    cap.release()

    scene_score = np.array(scene_score)
    processed_scene_score = (scene_score - np.min(scene_score)) / (np.max(scene_score) - np.min(scene_score))

    cursor = db.cursor()

    sql = f"ALTER TABLE {table_name} ADD COLUMN scene DOUBLE;"
    try:
        cursor.execute(sql)
        print(f"成功向表 {table_name} 添加列 scene。")
    except pymysql.Error as e:
        print(f"向表 {table_name} 添加列 scene 出错：{e}")

    data = list(zip(processed_scene_score))
    sql = f"UPDATE {table_name} SET scene = %s WHERE scene IS NULL LIMIT 1"
    try:
        for value in data:
            cursor.execute(sql, value)
            db.commit()
        print(f"成功插入数据到表 {table_name} 中的 scene 列。")
    except pymysql.Error as e:
        db.rollback()
        print(f"插入数据到表 {table_name} 中的 scene 列出错：{e}")

    cursor.close()
