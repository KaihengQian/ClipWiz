import cv2
import numpy as np


def fill_hole(mask):
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    len_contour = len(contours)
    contour_list = []
    for i in range(len_contour):
        drawing = np.zeros_like(mask, np.uint8)  # 创建一张纯黑色的图
        img_contour = cv2.drawContours(drawing, contours, i, (255, 255, 255), -1)
        contour_list.append(img_contour)

    out = sum(contour_list)
    return out


# 屏蔽掉非球场部分，可用deeplabv3+代替
def field_focus(frame):
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 只保留绿色范围
    lower_bound = np.array([35, 40, 40])
    upper_bound = np.array([65, 255, 255])
    temp_mask = cv2.inRange(frame1, lower_bound, upper_bound)
    # 滤波，去除噪声
    mask1 = cv2.GaussianBlur(temp_mask, (3, 3), 0)
    mask1 = cv2.bilateralFilter(mask1, 5, 150, 150)
    # 去噪后填充mask的孔洞
    mask2 = fill_hole(mask1)
    image, contours, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    n = len(contours)  # 轮廓的个数
    cv_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)  # 轮廓所围面积
        if area <= 100000:
            cv_contours.append(contour)
        else:
            continue
    mask3 = cv2.fillPoly(mask2, cv_contours, (255, 255, 255))
    # 三次腐蚀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
    mask = cv2.erode(mask3, kernel)
    mask = cv2.erode(mask, kernel)
    mask = cv2.erode(mask, kernel)
    # do masking
    frame2 = cv2.bitwise_and(frame, frame, mask=mask)
    return frame2


# 计算线段长度
def line_length(x1, y1, x2, y2):
    t = ((x1 - x2) ** 2) + ((y1 - y2) ** 2)
    return np.sqrt(t)


# 检测与中圈相交直线
def midfield_line_detect(frame):
    img = cv2.resize(frame, (512, 512))
    pic = field_focus(img)  # 可以用deeplabv3+模型代替这一步
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], mask=None, histSize=[256], ranges=[0, 255])
    hist = hist.reshape(-1)  # 变成行数组
    total = (gray.shape[0]) * (gray.shape[1])  # number of pixels

    # 根据灰度直方图，像素个数累加超过98%的灰度值作为二值化阈值m，剩余较亮的像素主要为场地白线
    sum = 0
    m = 0
    bound = 0.98 * total
    for i in range(256):
        sum += hist[i]
        if sum >= bound:
            m = i
            break

    # 二值化
    ret, pic1 = cv2.threshold(gray, m, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    for i in range(2):
        pic1 = cv2.dilate(pic1, kernel)
        pic1 = cv2.erode(pic1, kernel)
    # 找轮廓，继续分割
    pic2, contours, hierarchy = cv2.findContours(pic1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    drawing = np.zeros_like(pic, np.uint8)  # 创建一张纯黑色的底板
    cv2.drawContours(drawing, contours, -1, (255, 255, 255), 3)
    drawing = cv2.medianBlur(drawing, 3)
    for i in range(4):
        drawing = cv2.dilate(drawing, kernel)
        drawing = cv2.erode(drawing, kernel)
        drawing = cv2.medianBlur(drawing, 3)

    drawing = cv2.erode(drawing, kernel)
    pic3 = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
    ret, pic4 = cv2.threshold(pic3, 200, 255, cv2.THRESH_BINARY)
    # 检测直线
    lines = cv2.HoughLinesP(pic4, 1, np.pi / 180, threshold=150, minLineLength=200, maxLineGap=50)

    # 最小二乘拟合，留下中长线
    while lines is None:
        break
    else:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            loc = []
            loc.append([x1, y1])
            loc.append([x2, y2])
        loc = np.array(loc)
        output = cv2.fitLine(loc, cv2.DIST_L2, 0, 0.01, 0.01)
        k = output[1] / output[0]
        b = output[3] - k * output[2]
        pstart_y = 0
        pstart_x = 0
        pend_x = 0
        pend_y = 0
        if 0 <= b <= 512:
            pstart_y = b
            pstart = (0, pstart_y)
            pend_y = 512 * k + b
            pend = (512, pend_y)
            cv2.line(img, pstart, pend, (255, 0, 0), 2)
        else:
            pstart_x = (-b) / k
            pstart = (pstart_x, 0)
            pend_x = (512 - b) / k
            pend = (pend_x, 512)
            cv2.line(img, pstart, pend, (255, 0, 0), 2)

    return img
