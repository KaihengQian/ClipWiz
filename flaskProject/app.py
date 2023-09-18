import math
import os
import librosa
import pandas as pd
from flask import Flask, render_template, request, jsonify
from gevent import pywsgi
from soccer import soccer_audio_helper_functions, soccer_cv_helper_functions, soccer_other_helper_functions
from danmu import danmu_counts_helper_functions, danmu_emotion_helper_functions, danmu_highlights_play
import time
# from sqlalchemy import create_engine, text
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/user1')

app = Flask(__name__)

# Define a folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/bilibili', methods=['POST'])
def bilibili():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        text_content = request.form['text_content']

        if uploaded_file:
            filename = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(filename)

        if text_content:
            text_filename = os.path.join(UPLOAD_FOLDER, 'text_content.txt')
            with open(text_filename, 'w') as text_file:
                text_file.write(text_content)

        response = jsonify({"message": "Upload successful"})
        response.status_code = 200
        return response


@app.route('/football1')
def football1():
    return render_template('football.html')


@app.route('/football', methods=['POST'])
def football():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            filename = os.path.join(UPLOAD_FOLDER, 'raw_video.mp4')
            uploaded_file.save(filename)

        response = jsonify({"message": "Upload successful"})
        response.status_code = 200
        return response


@app.route('/loading')
def loading_page():
    return render_template('loading.html')


@app.route('/soccer', methods=['POST'])
def soccer():
    # 用户名和视频类别及编号
    user_name = "user1"
    video_name = "soccer1"
    list_name = "timelist1"

    # 保存路径
    raw_video_path = "uploads/raw_video.mp4"
    input_video_path = "uploads/video.mp4"
    audio_path = "uploads/audio.wav"
    output_video_path = "static/videos/highlights.mp4"

    weight_1 = 0.3937278703903585
    weight_2 = 0.868770984470414
    weight_3 = 0.6092057792177344

    # 视频预处理（剪切去除开球前的视频片段）
    soccer_cv_helper_functions.video_preprocess(raw_video_path, input_video_path)

    # 提取音频
    soccer_audio_helper_functions.audio_extract(input_video_path, audio_path)

    # 音频预处理
    duration = librosa.get_duration(filename=audio_path)
    audio, sample_rate = librosa.load(audio_path, sr=24000)  # 加载音频，设置采样率
    audio = soccer_audio_helper_functions.audio_pre_emphasis(audio, duration, sample_rate)  # 音频预加重
    time_slice = 5  # 将音频划分为时长均为5秒的块
    sample_number = time_slice * sample_rate  # 计算每一块的采样数（采样数=采样率*采样时间）
    block_number = math.ceil(len(audio) / sample_number)  # 计算块数量

    # 连接数据库
    database = soccer_other_helper_functions.connect_database(user_name, video_name, list_name)

    # 获取块的开始时间、结束时间信息
    soccer_other_helper_functions.block_time(block_number, database, video_name)

    # 获取块的能量信息
    soccer_audio_helper_functions.audio_energy(audio, sample_rate, sample_number, block_number, database, video_name)

    # 获取块的过零率信息
    soccer_audio_helper_functions.audio_zero_crossings(audio, sample_rate, sample_number, block_number, database, video_name)

    # 获取块的场景识别信息
    soccer_cv_helper_functions.video_scene(input_video_path, database, video_name)

    # 计算块的最终得分
    soccer_other_helper_functions.score_calculate(weight_1, weight_2, weight_3, database, video_name)

    # 获取所需块的时间序列
    soccer_other_helper_functions.get_time_list(database, video_name, list_name)

    # 剪辑原视频获得集锦
    soccer_other_helper_functions.video_edit(input_video_path, database, list_name, output_video_path)

    # 关闭数据库
    database.close()

    # 删除音频和视频文件
    os.remove(audio_path)
    os.remove(input_video_path)
    os.remove(raw_video_path)

    return


@app.route('/danmu', methods=['POST'])
def danmu():
    with open('uploads/text_content.txt', 'r') as file:
        video_url = file.read()

    # 在这里对用户输入进行处理
    # 通过视频链接获取弹幕数据
    danmu_counts_helper_functions.get_dm_to_csv(
        danmu_counts_helper_functions.cid_to_url(danmu_counts_helper_functions.bv_get_cid(video_url)))

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

    # 播放集锦
    return danmu_highlights_play.highlights_play(video_url)


server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
server.serve_forever()
