import cv2
import numpy as np
from threading import Thread, Event
import time
from ScreenCatcher import ScreenCatcher
import pyautogui
import PIL
from Redirector import Redirector

class VideoWriter:
    mouse = PIL.Image.open("Images\Mouse\mouse.png")
    def __init__(self, outputFile="video.avi", format="mp4v"):
        print("__init__ VW start")
        self.outputFile = outputFile
        self.format = cv2.VideoWriter_fourcc(*format)
        self.ev = Event()
        self.SC = ScreenCatcher(self.ev)
        while self.SC.bitrate == 0:
            pass
        self.WriteProcess = Thread(target=self.write)
        self.WriteProcess.start()
        print("__init__ VW complete")

    def write(self):
        self.ev.wait(1)
        print("start write")
        queue = self.SC.q.get()
        print(queue)
        a = cv2.cvtColor(np.array(queue[0]), cv2.COLOR_RGB2BGR)
        self.height, self.width, self.channels = a.shape
        self.out = cv2.VideoWriter(self.outputFile, self.format, self.SC.bitrate, (self.width, self.height))
        self.out.write(a)

        print("Bitrate : ", self.SC.bitrate)
        startTime = time.time() * 100
        curKey = None
        while not self.SC.q.empty():  # expression
            queue = self.SC.q.get()
            x, y = queue[1]
            ImgSize = 0
            keys = queue[2]
            while keys != []:
                x, y = queue[1]
                if not keys[0].find("_m"):
                    queue[0].paste(self.mouse, (x, y), self.mouse)
                    x, y = 25 + ImgSize, 900
                    img = PIL.Image.open("Images\\Keyboard\\{}.png".format(keys[0]))
                    ImgSize += 160
                    queue[0].paste(img, (x, y), img)
                else:
                    img = PIL.Image.open("Images\\Mouse\\{}.png".format(keys[0]))
                    queue[0].paste(img, (x, y), img)
                keys.pop([0])
            else:
                queue[0].paste(self.mouse, (x, y), self.mouse)
            queue[0] = cv2.cvtColor(np.array(queue[0]), cv2.COLOR_RGB2BGR)
            self.out.write(queue[0])
        endTime = time.time() * 100
        print("Work Time : ", endTime - startTime, "sec * 10^-2")
        self.save()

    def stop(self, expession):
        self.SC.expession = expession

    def save(self):
        #self.redirect.kill()
        self.out.release()
        cv2.destroyAllWindows()
