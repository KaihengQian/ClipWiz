from moviepy.editor import AudioFileClip


def soccer_audio_extract(video_path, save_path):
    my_audio_clip = AudioFileClip(video_path)
    my_audio_clip.write_audiofile(save_path)
