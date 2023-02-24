import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from moviepy import editor


def is_kick_off(frame):  # 检测开球帧
    return 1


def video_preprocess(raw_video_path, input_video_path):
    cap = cv2.VideoCapture(raw_video_path)
    frame_num = cap.get(7)  # 获取总帧数
    fps = cap.get(5)  # 获取帧率
    time_interval = 2  # 设置检测间隔（单位为秒）
    frame_interval = int(fps) * time_interval  # 将检测间隔按单位换算为帧数
    c = 0  # 当前所在帧
    while c < (frame_num * 0.2):
        ret, frame = cap.read()
        if ret:
            if (c % frame_interval) == 0:
                if is_kick_off(frame):
                    break
            c += 1
            cv2.waitKey(0)
        else:
            break
    cap.release()

    start_frame = c
    start_time = start_frame / fps
    raw_video = editor.VideoFileClip(raw_video_path)
    video = raw_video.subclip(t_start=start_time)
    video.write_videofile(input_video_path)

