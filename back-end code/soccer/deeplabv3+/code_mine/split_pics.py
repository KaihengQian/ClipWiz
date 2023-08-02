import cv2
import os

# 分割第一组图
path_phase1 = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/train_phase_1"
save_phase1_before = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/phase1_before"
save_phase1_after = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/phase1_after"
filelist1 = os.listdir(path_phase1)
num = len(filelist1)
for i in range(num):
    jpg_name = str(i + 1)
    if i <= 8:
        jpg_name = "00" + jpg_name + "_AB.jpg"
    elif 9 <= i <= 98:
        jpg_name = "0" + jpg_name + "_AB.jpg"
    else:
        jpg_name += "_AB.jpg"
    read_path = path_phase1 + "/" + jpg_name
    img = cv2.imread(read_path)
    # y0:y1, x0:x1
    pic1 = img[0:300, 0:300]
    pic2 = img[0:300, 300:600]
    pic2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)
    before_path = save_phase1_before + "/" + str(i + 1) + ".jpg"
    after_path = save_phase1_after + "/" + str(i + 1) + ".png"
    cv2.imwrite(before_path, pic1)
    cv2.imwrite(after_path, pic2)


# 分割第二组图
path_phase2 = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/train_phase_2"
save_phase2_before = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/phase2_before"
save_phase2_after = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/phase2_after"
filelist2 = os.listdir(path_phase2)
num = len(filelist2)
for i in range(num):
    jpg_name = str(i + 1)
    if i <= 8:
        jpg_name = "00" + jpg_name + "_AB.jpg"
    elif 9 <= i <= 98:
        jpg_name = "0" + jpg_name + "_AB.jpg"
    else:
        jpg_name += "_AB.jpg"
    read_path = path_phase2 + "/" + jpg_name
    img = cv2.imread(read_path)
    # y0:y1, x0:x1
    pic1 = img[0:300, 0:300]
    pic2 = img[0:300, 300:600]
    pic2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)
    before_path = save_phase2_before + "/" + str(i + 1) + ".jpg"
    after_path = save_phase2_after + "/" + str(i + 1) + ".png"
    cv2.imwrite(before_path, pic1)
    cv2.imwrite(after_path, pic2)


# 分割val
path_val = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/val"
save_val_before = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/val_before"
save_val_after = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/val_after"
filelist3 = os.listdir(path_val)
num = len(filelist3)
for i in range(num):
    jpg_name = str(i + 1)
    if i <= 8:
        jpg_name = "00" + jpg_name + "_AB.jpg"
    elif 9 <= i <= 98:
        jpg_name = "0" + jpg_name + "_AB.jpg"
    else:
        jpg_name += "_AB.jpg"
    read_path = path_val + "/" + jpg_name
    img = cv2.imread(read_path)
    # y0:y1, x0:x1
    pic1 = img[0:256, 0:256]
    pic2 = img[0:256, 256:512]
    pic2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)
    before_path = save_val_before + "/" + str(i + 1) + ".jpg"
    after_path = save_val_after + "/" + str(i + 1) + ".png"
    cv2.imwrite(before_path, pic1)
    cv2.imwrite(after_path, pic2)


# 分割test
path_test = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/test"
save_test_before = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/test_before"
save_test_after = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/test_after"

filelist4 = os.listdir(path_test)
num = len(filelist4)
for i in range(num):
    jpg_name = str(i + 1)
    if i <= 8:
        jpg_name = "00" + jpg_name + "_AB.jpg"
    elif 9 <= i <= 98:
        jpg_name = "0" + jpg_name + "_AB.jpg"
    else:
        jpg_name += "_AB.jpg"
    read_path = path_test + "/" + jpg_name
    img = cv2.imread(read_path)
    # y0:y1, x0:x1
    pic1 = img[0:256, 0:256]
    pic2 = img[0:256, 256:512]
    pic2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)
    before_path = save_test_before + "/" + str(i + 1) + ".jpg"
    after_path = save_test_after + "/" + str(i + 1) + ".png"
    cv2.imwrite(before_path, pic1)
    cv2.imwrite(after_path, pic2)

# 合并
num1 = len(filelist3)  # val
for i in range(num1):
    path_before = save_val_before + "/" + str(i + 1) + ".jpg"
    img = cv2.imread(path_before)
    before_path = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/before/" + str(i + 210) + ".jpg"
    cv2.imwrite(before_path, img)
    path_after = save_val_after + "/" + str(i + 1) + ".png"
    img1 = cv2.imread(path_after)
    after_path = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/after/" + str(i + 210) + ".png"
    cv2.imwrite(after_path, img1)

num2 = len(filelist4)  # test
for i in range(num2):
    path_before = save_test_before + "/" + str(i + 1) + ".jpg"
    img = cv2.imread(path_before)
    before_path = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/before/" + str(i + 419) + ".jpg"
    cv2.imwrite(before_path, img)
    path_after = save_test_after + "/" + str(i + 1) + ".png"
    img1 = cv2.imread(path_after)
    after_path = "D:/Pycharm/pythonProject/project/dataset/soccer_seg_detection/after/" + str(i + 419) + ".png"
    cv2.imwrite(after_path, img1)