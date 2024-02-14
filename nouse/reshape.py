import os
# os.chdir('/content/drive/MyDrive/Colab Notebooks')  # 使用 Colab 要換路徑使用

from moviepy.editor import *
video = VideoFileClip("./videos/0Foota1.mp4")    # 讀取影片
output = video.resize(width=400)           # 改變尺寸
output.write_videofile("./videos/0Foota1output.mp4", fps=30, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
print('ok')