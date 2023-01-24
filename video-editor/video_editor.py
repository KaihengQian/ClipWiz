import numpy as np
import pandas as pd
from moviepy import editor


def video_edit(input_video_path, time_list_path, output_video_path):
    video_input = editor.VideoFileClip(input_video_path)

    time_list = pd.read_csv(time_list_path)
    start_list = np.array(time_list['start'])
    end_list = np.array(time_list['end'])

    start = start_list[0]
    end = end_list[0]
    video_output = video_input.subclip(start, end)
    for i in range(1, len(start_list)):
        start = start_list[i]
        end = end_list[i]
        temp = video_input.subclip(start, end)
        video_output = editor.concatenate_videoclips([video_output, temp])

    video_output.write_videofile(output_video_path)

