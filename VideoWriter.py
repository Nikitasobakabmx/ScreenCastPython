import cv2
import numpy as np
import os
import pyautogui

class VideoWriter:
    def __init__(self, output = "video.avi", format = "mp4v"):
        self.output = output
        self.format = cv2.VideoWriter_fourcc(*format)
        self.height, self.width, self.channels = self.img.shape
        self.out = cv2.VideoWriter(self.output, self.format, 20.0, (self.width, self.height))
    def write(self, imgList):
        for img in imgList:
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            self.out.write(image)
    def __del__(self):
        out.release()
        cv2.destroyAllWindows()

        