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
        self.processes = []
        self.q = Queue()
        for _ in range(4):
            self.processes.append(Process(target = self.shot))#args = self maybe
        for process in self.processes:
            process.start()
        time.sleep(1)
        self.bitrate = int(self.q.qsize() - self.q.qsize()/15) #magic 
    def shot(self):
        while True: #(time.time()*100 - startTime) < 95:
            a = pyautogui.screenshot()
            self.q.put({"pic" : a, "time" : time.time()*100})
    def terminate(self):
        for process in self.processes:
            process.terminate()
class VideoWriter:
    
    def __init__(self, outputFile = "video.avi", format = "mp4v"):
        self.outputFile = outputFile
        self.format = cv2.VideoWriter_fourcc(*format)
        self.SC = ScreenCatcher()
        self.bitrate = self.SC.bitrate
        self.WriteProcess = Process(target = self.write, args = (self.SC.q, ))

    def write(self, q):
        a = q.get()
        a = cv2.cvtColor(np.array(a["pic"]), cv2.COLOR_RGB2BGR)
        self.height, self.width, self.channels  = a.shape
        self.out = cv2.VideoWriter(self.outputFile, self.format, self.bitrate, (self.width, self.height))
        self.out.write(a)
        startTime = timt.time() * 100
        while (timt.time() * 100 - startTime) < 500: #expression
            a = q.get()
            a = cv2.cvtColor(np.array(a["pic"]), cv2.COLOR_RGB2BGR)
            self.out.write(a)
        self.save()
        self.SC.terminate()
    def save(self):
        self.out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    
    vW = VideoWriter()
    vW.write()