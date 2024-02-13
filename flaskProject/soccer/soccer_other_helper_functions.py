import os
import shutil
import numpy as np
import math
from moviepy import editor
import pymysql


def create_subfolder(home_folder_path, subfolder_name):
    subfolder_path = home_folder_path + "./" + subfolder_name
    if os.path.exists(subfolder_path):  # 检测要创建的子文件夹是否已经存在
        print("The folder already exists.")
        shutil.rmtree(subfolder_path)  # 删除已经存在的子文件夹
    os.mkdir(subfolder_path)
    subfolder_path = os.path.join(home_folder_path, subfolder_name)
    file_name = ["./data", "./result", "./graph"]
    for name in file_name:
        os.mkdir(subfolder_path + name)
    return subfolder_path


def connect_database(db_name, table_name_1, table_name_2):
    db = pymysql.connect(host="localhost", port=3306, user="root", password="qkh123456", database=db_name)
    cursor = db.cursor()

    # 检测是否成功连接数据库
    sql = "SELECT VERSION();"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)

    # 在数据库中创建两张表
    sql = f"CREATE TABLE IF NOT EXISTS {table_name_1} (id INT AUTO_INCREMENT PRIMARY KEY);"
    try:
        cursor.execute(sql)
        print(f"成功创建表 {table_name_1}。")
    except pymysql.Error as e:
        print(f"创建表 {table_name_1} 出错：{e}")
    sql = f"CREATE TABLE IF NOT EXISTS {table_name_2} (id INT AUTO_INCREMENT PRIMARY KEY);"
    try:
        cursor.execute(sql)
        print(f"成功创建表 {table_name_2}。")
    except pymysql.Error as e:
        print(f"创建表 {table_name_2} 出错：{e}")

    cursor.close()
    return db


def block_time(block_number, db, table_name):
    cursor = db.cursor()

    sql = f"ALTER TABLE {table_name} ADD COLUMN start INT, ADD COLUMN end INT;"
    try:
        cursor.execute(sql)
        print(f"成功向表 {table_name} 添加列 start 和 end。")
    except pymysql.Error as e:
        print(f"向表 {table_name} 添加列 start 和 end 出错：{e}")

    start_list = [5 * x for x in range(block_number)]
    end_list = [5 * (x + 1) for x in range(block_number)]
    data = list(zip(start_list, end_list))
    sql = f"INSERT INTO {table_name} (start, end) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, data)
        db.commit()
        print(f"成功插入数据到表 {table_name} 中的多列。")
    except pymysql.Error as e:
        db.rollback()
        print(f"插入数据到表 {table_name} 中的多列出错：{e}")

    cursor.close()


def score_calculate(weight_1, weight_2, weight_3, db, table_name):
    cursor = db.cursor()

    sql = f"ALTER TABLE {table_name} ADD COLUMN score DOUBLE;"
    try:
        cursor.execute(sql)
        print(f"成功向表 {table_name} 添加列 score。")
    except pymysql.Error as e:
        print(f"向表 {table_name} 添加列 score 出错：{e}")

    sql = f"UPDATE {table_name} SET score = (energy * {weight_1}) + (zero_crossings * {weight_2}) + (scene * {weight_3})"
    try:
        cursor.execute(sql)
        db.commit()  # Commit the changes to the database
        print(f"成功插入数据到表 {table_name} 中的 score 列。")
    except pymysql.Error as e:
        db.rollback()  # Rollback the changes if there's an error
        print(f"插入数据到表 {table_name} 中的 score 列出错：{e}")

    cursor.close()


def get_time_list(db, table_name_1, table_name_2):
    cursor = db.cursor()

    # 根据得分筛选得到所需块
    sql = f"SELECT score FROM {table_name_1}"
    try:
        cursor.execute(sql)
        column_data = [row[0] for row in cursor.fetchall()]
        score = np.array(column_data)
        print(f"成功从表 {table_name_1} 中取出 score 列。")
    except pymysql.Error as e:
        print(f"从表 {table_name_1} 中取出 score 列时出错：{e}")
        return
    sorted_score = sorted(score)
    threshold_rate = 0.96  # 设置阈值以筛选得分最高的4%的块
    threshold = sorted_score[math.ceil(threshold_rate * len(sorted_score))]

    sql = f"SELECT start FROM {table_name_1}"
    try:
        cursor.execute(sql)
        column_data = [row[0] for row in cursor.fetchall()]
        start = np.array(column_data)
        print(f"成功从表 {table_name_1} 中取出 start 列。")
    except pymysql.Error as e:
        print(f"从表 {table_name_1} 中取出 start 列时出错：{e}")
        return
    sql = f"SELECT end FROM {table_name_1}"
    try:
        cursor.execute(sql)
        column_data = [row[0] for row in cursor.fetchall()]
        end = np.array(column_data)
        print(f"成功从表 {table_name_1} 中取出 end 列。")
    except pymysql.Error as e:
        print(f"从表 {table_name_1} 中取出 end 列时出错：{e}")
        return

    start_list = []
    end_list = []
    start_list.append(start[0])
    end_list.append(end[0])
    for i in range(len(score) - 1):
        if score[i + 1] >= threshold:
            start_list.append(start[i + 1])
            end_list.append(end[i + 1])

    # 合并时间相邻的块，更新时间序列
    tmp_start = []
    tmp_end = []
    i = 0
    j = 0
    m = len(start_list) - 2
    n = len(start_list) - 1
    while i <= m:
        tmp_start.append(start_list[i])
        j = i + 1
        while j <= n:
            if end_list[i] == start_list[j]:
                i = j
                j += 1
                if j > n:
                    tmp_end.append(end_list[i - 1])
            else:
                tmp_end.append(end_list[i])
                i = j
                break

    # 考虑反应时间，将块的开始时间相应提前
    response_time = 5
    for i in range(len(tmp_start)):
        if tmp_start[i] >= response_time:
            tmp_start[i] -= response_time

    sql = f"ALTER TABLE {table_name_2} ADD COLUMN start INT, ADD COLUMN end INT;"
    try:
        cursor.execute(sql)
        print(f"成功向表 {table_name_2} 添加列 start 和 end。")
    except pymysql.Error as e:
        print(f"向表 {table_name_2} 添加列 start 和 end 出错：{e}")

    sql = f"DELETE FROM {table_name_2}"
    try:
        cursor.execute(sql)
        db.commit()
        print(f"成功清空表 {table_name_2} 中的内容。")
    except pymysql.Error as e:
        db.rollback()
        print(f"清空表 {table_name_2} 中的内容出错：{e}")

    data = list(zip(tmp_start, tmp_end))

    sql = f"INSERT INTO {table_name_2} (start, end) VALUES (%s, %s)"
    try:
        cursor.executemany(sql, data)
        db.commit()
        print(f"成功插入数据到表 {table_name_2} 中的多列。")
    except pymysql.Error as e:
        db.rollback()
        print(f"插入数据到表 {table_name_2} 中的多列出错：{e}")

    cursor.close()


def video_edit(input_video_path, db, table_name, output_video_path):
    video_input = editor.VideoFileClip(input_video_path)

    cursor = db.cursor()

    sql = f"SELECT start FROM {table_name}"
    try:
        cursor.execute(sql)
        column_data = [row[0] for row in cursor.fetchall()]
        start_list = np.array(column_data)
        print(f"成功从表 {table_name} 中取出 start 列。")
    except pymysql.Error as e:
        print(f"从表 {table_name} 中取出 start 列时出错：{e}")
        return
    sql = f"SELECT end FROM {table_name}"
    try:
        cursor.execute(sql)
        column_data = [row[0] for row in cursor.fetchall()]
        end_list = np.array(column_data)
        print(f"成功从表 {table_name} 中取出 end 列。")
    except pymysql.Error as e:
        print(f"从表 {table_name} 中取出 end 列时出错：{e}")
        return

    cursor.close()

    start = start_list[0]
    end = end_list[0]
    video_output = video_input.subclip(start, end)
    for i in range(1, len(start_list)):
        start = start_list[i]
        end = end_list[i]
        temp = video_input.subclip(start, end)
        video_output = editor.concatenate_videoclips([video_output, temp])

    video_output.write_videofile(output_video_path)
