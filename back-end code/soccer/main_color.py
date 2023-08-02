import cv2
import extcolors
from PIL import Image
import numpy as np


# rgb和hsv数值转换
def rgb2hsv(r, g, b):
    h = 0
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df / mx
    v = mx
    return h, s, v


# 判断是否在球场上（主色为绿色）
def main_color_extract(frame):
    # resize
    output_width = 900
    wpercent = output_width / (float(frame.shape[1]))
    hsize = int(float(frame.shape[0]) * float(wpercent))
    frame_now = cv2.resize(frame, (output_width, hsize), interpolation=cv2.INTER_AREA)
    frame_now = Image.fromarray(frame_now)
    # 提取主色并判断
    main_color = extcolors.extract_from_image(frame_now, tolerance=12, limit=1)
    list1 = main_color[0]
    list2 = list(list1[0])
    color_array = np.array(list2[0])
    h, s, v = rgb2hsv(color_array[0], color_array[1], color_array[2])
    if 150 <= h < 210:
        return 1
    else:
        return 0
