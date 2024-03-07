import os
from moviepy.editor import *
from moviepy.video.fx.resize import resize
from moviepy.editor import VideoFileClip, vfx
from nouse.zoom import zoom
import cv2
import numpy as np

def optimize_video_picture_allocation(selected_videos, selected_pictures, durations):
    # 初始化字典：为每个持续时间创建空列表
    video_dict = {str(key): [] for key in range(len(durations))}
    picture_dict = {str(key): [] for key in range(len(durations))}

    # 分配视频到对应的类别
    for video_file in selected_videos:
        key = video_file[0]  # 假设类别标识符是字符串的第一个字符
        if key in video_dict:
            video_dict[key].append(video_file)

    # 分配图片到对应的类别
    for picture_file in selected_pictures:
        key = picture_file[0]  # 同样假设类别标识符是字符串的第一个字符
        if key in picture_dict:
            picture_dict[key].append(picture_file)

    # 转换字典值为列表
    video_list = list(video_dict.values())
    picture_list = list(picture_dict.values())

    # 打印结果以验证
    print("Video List:", video_list)
    print("Picture List:", picture_list)

    # 返回结果，以便可以在其他地方使用
    return video_list, picture_list


def resize_frame(frame, target_width, target_height):
    return cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)

def zoom_in_memory(height, width, image_path, total_frames):
    zoom_frames = []  # 存储所有缩放帧的列表
    print(image_path)
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("Image could not be read.")
    

    # 为简化，我们只示范放大的部分
    for scale in np.linspace(1, 1.5, total_frames):  # 从1倍放大到1.5倍，总共60帧
        frame_width, frame_height = int(width * scale), int(height * scale)
        resized = cv2.resize(img, (frame_width, frame_height))
        
        # 将缩放后的图像裁剪或填充到原始尺寸
        if scale > 1:
            start_row = (frame_height - height) // 2
            start_col = (frame_width - width) // 2
            frame = resized[start_row:start_row+height, start_col:start_col+width]
        else:
            frame = cv2.copyMakeBorder(resized, 0, height - frame_height, 0, width - frame_width, cv2.BORDER_CONSTANT)
        
        zoom_frames.append(frame)

    return zoom_frames

def merge_videos(selected_videos, selected_pictures, durations, size):

    video_list, picture_list = optimize_video_picture_allocation(selected_videos, selected_pictures, durations)

    fps = 24
    width, height = map(int, size.split('x'))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('./videos/output_cv2.mp4', fourcc, fps, (width, height))

    audio_list = []

    for i, duration in enumerate(durations):
        print(video_list[i])
        if len(video_list[i]) > 0:
            audio = AudioFileClip('./speeches/' + video_list[i][0][0] + '.mp3')
        else:
            audio = AudioFileClip('./speeches/' + picture_list[i][0][0] + '.mp3')

        if duration == 0:
            duration = audio.duration
            durations[i] = duration
        video_duration = duration / (len(video_list[i]) + len(picture_list[i]))
        total_frames = int(fps * video_duration)  # 计算总帧数

        audio_list.append(audio.set_start(0) if i == 0 else audio.set_start(durations[i - 1]))
        print(audio.duration, duration)
        # Process videos
        for video_file in video_list[i]:
            cap = cv2.VideoCapture('./videos/' + video_file + '.mp4')
            count = 0  # 计数器，跟踪已处理的帧数
            while cap.isOpened() and count < total_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = resize_frame(frame, width, height)
                
                cv2.putText(frame, text="This video contains AI-generated content.", 
                            org=(00, 0) , fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                            color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
                out.write(frame)
                count += 1
        # Process pictures
        frames = []
        for picture_file in picture_list[i]:
            # Assuming `zoom` function adapts the image and saves a temporary zoomed version
            zoomed_image_path = './pictures/' + picture_file + '.png'
            # 生成视频帧
            frames = zoom_in_memory(height=height, width=width, image_path=zoomed_image_path, total_frames=total_frames)
            for frame in frames:
                cv2.putText(frame, text="This video contains AI-generated content.", 
                            org=(0, 0) , fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                            color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
                out.write(frame)
    out.release()
    cv2.destroyAllWindows()

    video = VideoFileClip("./videos/output_cv2.mp4")


    # 将音频片段合并成一个音频剪辑
    final_audio = CompositeAudioClip(audio_list)

    # 将合并后的音频添加到视频中
    final_video = video.set_audio(final_audio)

    # 输出最终的视频文件
    final_video.write_videofile("./videos/target.mp4", codec="libx264", audio_codec="aac")
        


if __name__ == '__main__':
    selected_videos = ['00', '10']
    selected_videos = []
    selected_pictures = ['00', '01', '02', '10', '11', '12']
    durations = [19, 17]
    size = '1080 x 1920'
    # size = '1920 x 1080'
    merge_videos(selected_videos, selected_pictures, durations, size)
