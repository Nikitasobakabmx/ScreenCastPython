import cv2
import numpy as np
from threading import Thread
import time
from ScreenCatcher import ScreenCatcher

class VideoWriter:
    def __init__(self, outputFile="video.avi", format="mp4v"):
        print("__init__ VW start")
        self.outputFile = outputFile
        self.format = cv2.VideoWriter_fourcc(*format)
        self.SC = ScreenCatcher()
        self.SC.expression = True
        self.threadSC = Thread(target = self.SC.start)
        self.WriteProcess = Thread(target=self.write)
        self.WriteProcess.start()
        print("__init__ VW complete")

    def write(self):
        print("start write")
        pic = self.SC.q.get()
        print(pic)
        pic = pic["pic"]
        a = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2BGR)
        self.height, self.width, self.channels = a.shape
        self.out = cv2.VideoWriter(self.outputFile, self.format, self.SC.bitrate, (self.width, self.height))
        self.out.write(a)

        print("Bitrate : ", self.SC.bitrate)
        i = 0
        startTime = time.time() * 100
        while not self.SC.q.empty():  # expression
            pic = self.SC.q.get()
            a = cv2.cvtColor(np.array(pic["pic"]), cv2.COLOR_RGB2BGR)
            self.out.write(a)
            i += 1
        endTime = time.time() * 100
        print("Work Time : ", endTime - startTime, "sec * 10^-2")
        self.save()

    def stop(self, expession):
        self.SC.expession = expession

    def save(self):
        self.out.release()
        cv2.destroyAllWindows()