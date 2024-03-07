import cv2
import numpy as np


fps = 30
def zoom(height, width, image_path, videopath='./videos'):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(videopath + 'out.mp4', fourcc, fps, (width, height), isColor=True)

    img=cv2.imread(image_path)

    background = np.full((height, width, 3), 0, np.uint8)

    for w in range(int(width * 3 / 4), int(width * 4 / 3), 2):
        h = int(height / width * w)
        scaleImg = cv2.resize(img, (w, h))
        if w <= width:
            offset_h = int((height - h) / 2)
            offset_w = int((width - w) / 2)
            frame = background.copy()
            frame[offset_h:offset_h + h, offset_w:offset_w + w] = scaleImg
        else:
            offset_h = int((h - height) / 2)
            offset_w = int((w - width) / 2)
            frame = background.copy()
            frame[:height, :width] = scaleImg[offset_h:offset_h + height, offset_w:offset_w + width]
        videoWriter.write(frame)

    videoWriter.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    zoom(1792, 1024, './pictures/00.png')