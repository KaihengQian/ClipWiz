import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


class DanmuHighlights(object):
    def __init__(self, start, end, video_duration):
        self.start = start
        self.end = end
        self.video_duration = video_duration
        s = Service('C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\edgedriver_win64\\msedgedriver.exe')
        self.driver = webdriver.Edge(service=s)

    def video_play(self):
        self.driver.get("file:///D:/Code/Project/front-end code/danmu/danmu_highlights_play.html")
        self.driver.maximize_window()
        y = 350
        for i in range(len(self.start)):
            play_start = self.start[i]
            play_end = self.end[i]
            play_time = play_end - play_start
            ele = self.driver.find_element(By.ID, "bilibili_frame")  # 查找iframe标签元素
            self.driver.switch_to.frame(ele)
            video_ele = self.driver.find_element(By.TAG_NAME, "video")  # 查找video标签元素
            action = ActionChains(self.driver)
            # move_to_element_with_offset方法以元素中心为基准进行偏移，在计算横坐标x时要减去元素宽度的一半
            x = video_ele.rect["width"] * (play_start / self.video_duration) - video_ele.rect["width"] / 2
            action.move_to_element_with_offset(video_ele, x, y).click().perform()
            action.click(video_ele).perform()  # 点击播放
            time.sleep(play_time)
        self.driver.quit()


def highlights_play(time_list_path):
    time_list = pd.read_csv(time_list_path)
    start_list = np.array(time_list['start'])
    end_list = np.array(time_list['end'])

    # danmu = pd.read_csv(danmu_path)
    # elapse_time = np.array(danmu['elapse_time'])
    # video_duration = max(elapse_time)

    test = DanmuHighlights(start_list, end_list, 993)
    test.video_play()


time_list_path = r"D:\Code\Project\User\User_1\result\time_list.csv"
# danmu_path = r""
highlights_play(time_list_path)
