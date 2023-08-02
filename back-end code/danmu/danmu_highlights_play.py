import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By


class DanmuHighlights(object):
    def __init__(self, start, end, video_url):
        self.start = start
        self.end = end
        self.video_url = video_url
        s = Service('C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\edgedriver_win64\\msedgedriver.exe')
        options = Options()
        options.add_argument("--start-maximized")  # 添加最大化窗口运作参数
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏“Microsoft Edge正由自动测试软件控制”的提示
        # options.add_argument(r'-user-data-dir=C:\Users\user\AppData\Local\Microsoft\Edge\User Data')
        self.driver = webdriver.Edge(service=s, options=options)

    def video_play(self):
        self.driver.get(self.video_url)
        time.sleep(1)  # 必须添加此行代码，等待视频加载完成
        video_ele = self.driver.find_element(By.TAG_NAME, "video")  # 查找video标签元素
        self.driver.execute_script("arguments[0].pause()", video_ele)  # 打开视频后先将其暂停
        while video_ele.get_attribute("paused") == "true":  # 等待用户播放视频
            video_ele = self.driver.find_element(By.TAG_NAME, "video")  # 更新video标签元素
            time.sleep(0.1)
        for i in range(len(self.start)):
            play_start = self.start[i]
            play_end = self.end[i]
            play_time = play_end - play_start
            execute_command = "arguments[0].currentTime = " + str(play_start) + ";"
            self.driver.execute_script(execute_command, video_ele)  # 模拟拉动进度条
            time.sleep(play_time)  # 播放集锦片段
        # 在退出之前先停住画面一小段时间
        video_ele.click()
        time.sleep(5)
        self.driver.quit()


def highlights_play(time_list_path, video_url):
    time_list = pd.read_csv(time_list_path)
    start_list = np.array(time_list['start'])
    end_list = np.array(time_list['end'])
    test = DanmuHighlights(start_list, end_list, video_url)
    test.video_play()

