import cv2
import os
from multiprocessing import Process, Queue
import numpy as np
import pyautogui
from PIL import Image
from pynput import keyboard, mouse
import time


class ScreenCatcher:
    def __init__(self):
        print("__init__ SC start")
        self.processes = []
        self.q = Queue()
        for _ in range(4):
            self.processes.append(Process(target=self.shot))  # args = self maybe
        for process in self.processes:
            process.start()
        time.sleep(1)
        self.bitrate = int(self.q.qsize() - self.q.qsize() / 15)  # magic
        print("__init__ SC complete")

    def shot(self):
        while True:  # (time.time()*100 - startTime) < 95:
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100})

    def terminate(self):
        for process in self.processes:
            process.terminate()


class VideoWriter:
    def __init__(self, outputFile="video.avi", format="mp4v"):
        print("__init__ VW start")
        self.outputFile = outputFile
        self.format = cv2.VideoWriter_fourcc(*format)
        self.SC = ScreenCatcher()
        self.bitrate = self.SC.bitrate
        self.WriteProcess = Process(target=self.write)
        self.WriteProcess.start()
        print("__init__ VW complete")

    def write(self):
        pic = self.SC.q.get()
        print(pic)
        pic = pic["pic"]
        a = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2BGR)
        self.height, self.width, self.channels = a.shape
        self.out = cv2.VideoWriter(self.outputFile, self.format, self.bitrate, (self.width, self.height))
        self.out.write(a)
        startTime = time.time() * 100
        print("Bitrate : ", self.bitrate)
        while (time.time() * 100 - startTime) < 500:  # expression
            pic = self.SC.q.get()
            pic = pic["pic"]
            a = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2BGR)
            self.out.write(a)
        self.save()
        self.SC.terminate()

    def save(self):
        self.out.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    vW = VideoWriter()