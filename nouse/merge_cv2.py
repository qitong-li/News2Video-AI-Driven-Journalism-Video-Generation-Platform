import cv2
import numpy as np
from nouse.zoom import zoom  # Ensure this is adapted for OpenCV as discussed earlier

def resize_frame(frame, target_width, target_height):
    return cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)

def merge_videos_cv2(selected_videos, selected_pictures, durations, target_resolution):
    width, height = map(int, target_resolution.split('x'))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('./videos/output_cv2.mp4', fourcc, 24, (width, height))

    # Process videos
    for video_file in selected_videos:
        cap = cv2.VideoCapture('./videos/' + video_file + '.mp4')
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = resize_frame(frame, width, height)
            out.write(frame)
        cap.release()

    # Process pictures
    for picture_file in selected_pictures:
        # Assuming `zoom` function adapts the image and saves a temporary zoomed version
        zoomed_image_path = zoom(height, width, './pictures/' + picture_file + '.png')
        image = cv2.imread(zoomed_image_path)
        frame = resize_frame(image, width, height)
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    selected_videos = ['00', '10']
    selected_pictures = ['00', '01', '02', '10', '11', '12']
    durations = [19, 17]  # Unused in this simplified example
    size = '1920x1080'
    merge_videos_cv2(selected_videos, selected_pictures, durations, size)
