import cv2
from Redirector import Redirector
import numpy as np
from threading import Thread
import time
from ScreenCatcher import ScreenCatcher
import pyautogui
import PIL
import Redirector

class VideoWriter:
    mouse = PIL.Image.open("Images\Mouse\mouse.png")
    def __init__(self, outputFile="video.avi", format="mp4v"):
        print("__init__ VW start")
        self.outputFile = outputFile
        self.format = cv2.VideoWriter_fourcc(*format)
        self.SC = ScreenCatcher()
        self.SC.expression = True
        self.Red = Redirector()
        self.threadSC = Thread(target = self.SC.start)
        self.threadSC.start()
        self.redirect = Redirect()
        self.threadRedirect = Thread(target = self.redirect.start)
        while self.SC.bitrate == 0:
            pass
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
        startTime = time.time() * 100
        previousPic = self.SC.q.get()
        curKey = None
        keys = []
        while not self.SC.q.empty():  # expression
<<<<<<< HEAD
            pic = previousPic
              not self.redirect.event.empty():
                key = self.redirect.event.get()
                while
            previousPic = self.SC.q.get()
            x, y = pyautogui.position()
            pic['pic'].paste(self.mouse, (x, y), self.mouse)
            pic = cv2.cvtColor(np.array(pic["pic"]), cv2.COLOR_RGB2BGR)
            self.out.write(pic)
=======
            pic = self.SC.q.get()
            if True:
                red = self.Red.event.get()
                if red['but'] != None:
                    if red['press'] == 'Pressed' or red['press'] == False:
                        x, y = red['pos'][0], red['pos'][1]
                        img_now = PIL.Image.open('{}.png'.format(red['but']))
                        print(img_now)
                        pic['pic'].paste(img_now, (x, y), img_now)
                        pic = cv2.cvtColor(np.array(pic["pic"]), cv2.COLOR_RGB2BGR)
                        self.out.write(pic)
                    else:
                        x, y = pyautogui.position()
                        pic['pic'].paste(self.mouse, (x, y), self.mouse)
                        pic = cv2.cvtColor(np.array(pic["pic"]), cv2.COLOR_RGB2BGR)
                        self.out.write(pic)
            else:
                x, y = pyautogui.position()
                pic['pic'].paste(self.mouse, (x, y), self.mouse)
                pic = cv2.cvtColor(np.array(pic["pic"]), cv2.COLOR_RGB2BGR)
                self.out.write(pic)
>>>>>>> 7e34825809eebe9b0eef195e5dd826166f040aa1
        endTime = time.time() * 100
        print("Work Time : ", endTime - startTime, "sec * 10^-2")
        self.save()

    def stop(self, expession):
        self.SC.expession = expession

    def save(self):
        self.out.release()
        cv2.destroyAllWindows()

vw = VideoWriter()
for i in range(100):
    vw.write()
vw.stop()
vw.save()
