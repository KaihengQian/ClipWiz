import os
import shutil


def create_subfolder(home_folder_path, subfolder_name):
    subfolder_path = home_folder_path + "./" + subfolder_name
    if os.path.exists(subfolder_path):  # 检测要创建的子文件夹是否已经存在
        print("The folder already exists.")
        shutil.rmtree(subfolder_path)  # 删除已经存在的子文件夹
    os.mkdir(subfolder_path)
    subfolder_path = os.path.join(home_folder_path, "./" + subfolder_name)
    file_name = ["./data", "./result", "./graph"]
    for name in file_name:
        os.mkdir(subfolder_path + name)
    return subfolder_path
