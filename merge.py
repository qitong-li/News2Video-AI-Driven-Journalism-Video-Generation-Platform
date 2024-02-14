from moviepy.editor import *
def merge_videos(selected_videos):
    result_dict = {}
    L = []
    for videofile in selected_videos:
        key = videofile[0]
        if key not in result_dict:
            result_dict[key] = []  # 如果字典中不存在该键，则创建一个空列表
        result_dict[key].append(videofile)
    print(result_dict)
    result_list = list(result_dict.values())  # 提取字典的值作为结果列表
    print(result_list)  
    for part in result_list:
        P = []
        audio = AudioFileClip('./speeches/' + part[0][0] + '.mp3')
        print(audio.duration)
        video_duration = audio.duration / len(part)
        # video_duration = 1
        for vi in part:
            filepath = './videos/' + vi + '.mp4'
            print(filepath)
            video_clip = VideoFileClip(filepath, audio=False, target_resolution=(1920, 1080))
            if video_clip.duration < video_duration:
                video_clip = video_clip.loop(duration = video_duration)
            else:
                video_clip = video_clip.subclip(0, video_duration)
            P.append(video_clip)
        final_clip = concatenate_videoclips(P)
        final_clip = final_clip.set_audio(audio)
        final_clip.to_videofile("./videos/" + part[0][0] + ".mp4", fps=24, remove_temp=False)
    
    for part in result_list:
        video = VideoFileClip('./videos/' + part[0][0] + '.mp4')
        L.append(video)
    
    final_clip = concatenate_videoclips(L)
    final_clip.to_videofile("./videos/target.mp4", fps=24, remove_temp=False)
        




if __name__ == '__main__':
    selected_videos = ['00', '01', '10']
    merge_videos(selected_videos)
