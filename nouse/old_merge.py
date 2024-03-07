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

def zoom_in_memory(height, width, image_path):
    fps = 30  # 帧率
    zoom_frames = []  # 存储所有缩放帧的列表
    print(image_path)
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image could not be read.")

    # 为简化，我们只示范放大的部分
    for scale in np.linspace(1, 1.5, 60):  # 从1倍放大到1.5倍，总共60帧
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

def frames_to_video(frames, output_path, fps=30, size=(1920, 1080)):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, size)
    for frame in frames:
        out.write(frame)
    out.release()


def merge_videos(selected_videos, selected_pictures, durations, size):

    video_list, picture_list = optimize_video_picture_allocation(selected_videos, selected_pictures, durations)

    L = []
    fps = 30

    for i, duration in enumerate(durations):
        P = []
        print(video_list[i])
        if len(video_list[i]) > 0:
            audio = AudioFileClip('./speeches/' + video_list[i][0][0] + '.mp3')
        else:
            audio = AudioFileClip('./speeches/' + picture_list[i][0][0] + '.mp3')

        print(audio.duration, duration)

        if duration == 0:
            duration = audio.duration
        video_duration = duration / (len(video_list[i]) + len(picture_list[i]))

        width, height = map(int, size.split('x'))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('./videos/output_cv2.mp4', fourcc, 24, (width, height))
        # Process videos
        for video_file in video_list[i]:
            cap = cv2.VideoCapture('./videos/' + video_file + '.mp4')
            total_frames = int(fps * video_duration)  # 计算总帧数
            count = 0  # 计数器，跟踪已处理的帧数
            while cap.isOpened() and count < total_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = resize_frame(frame, width, height)
                out.write(frame)
                count += 1
        '''
        # for vi in video_list[i]:
        #     filepath = './videos/' + vi + '.mp4'
        #     print(filepath)
        #     video_clip = VideoFileClip(filepath, audio=False, target_resolution=(1920, 1080))
        #     if video_clip.duration < video_duration:
        #         video_clip = video_clip.loop(duration = video_duration)
        #     else:
        #         video_clip = video_clip.subclip(0, video_duration)
        #     P.append(video_clip)
    
        # for pi in picture_list[i]:
        #     filepath = './pictures/' + pi + '.png'
        #     zoom(size[0], size[1], image_path=filepath)
        #     print(filepath)
        #     image_clip = ImageClip(filepath, duration=video_duration) 
        #     black_image = (ImageClip("./pictures/black_picture_1920x1080.png", duration=video_duration))
        #     image_clip = CompositeVideoClip([black_image, image_clip.set_position("center")])
        #     # image_clip = image_clip = resize(image_clip, width=1920, height=1080)
        '''
        # Process pictures
        frames = []
        for picture_file in picture_list[i]:
            # Assuming `zoom` function adapts the image and saves a temporary zoomed version
            zoomed_image_path = './pictures/' + picture_file + '.png'
            # 生成视频帧
            frames = zoom_in_memory(1080, 1920, zoomed_image_path)
            for frame in frames:
                out.write(frame)
        out.release()
        cv2.destroyAllWindows()


        # final_clip = concatenate_videoclips(P)
        # final_clip = final_clip.set_audio(audio)
        # final_clip.to_videofile("./videos/" + video_list[i][0][0] + ".mp4", fps=24, remove_temp=False)

    # # Generate a text clip  
    # txt_clip = TextClip("GeeksforGeeks", fontsize = 75, color = 'black')  
        
    # # setting position of text in the center and duration will be 10 seconds  
    # txt_clip = txt_clip.set_pos('center').set_duration(10)  
        



    # for part in video_list:
    #     video = VideoFileClip('./videos/' + part[0][0] + '.mp4')
    #     L.append(video)
    # if len(L) > 0:
    #     final_clip = concatenate_videoclips(L)
    #     # Generate a text clip  
    #     txt_clip = TextClip("GeeksforGeeks", fontsize = 75, color = 'black')  
            
    #     # setting position of text in the center and duration will be 10 seconds  
    #     txt_clip = txt_clip.set_pos('center').set_duration(10)

    #     # Overlay the text clip on the first video clip  
    #     video = CompositeVideoClip([final_clip, txt_clip])  
    #     final_clip.to_videofile("./videos/target.mp4", fps=24, remove_temp=False)
        


if __name__ == '__main__':
    selected_videos = ['00', '10']
    selected_videos = []
    selected_pictures = ['00', '01', '02', '10', '11', '12']
    durations = [19, 17]
    size = '1080 x 1920'
    merge_videos(selected_videos, selected_pictures, durations, size)
