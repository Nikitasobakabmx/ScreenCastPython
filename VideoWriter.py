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
        self.redirect = Redirector()
        self.shotEvent = Event()
        self.SC = ScreenCatcher(self.redirect, self.shotEvent)
        self.SC.expression = True
        
        
        #trading KeyBoard and mouse
        self.threadRedirect = Thread(target = self.redirect.start)
        self.threadRedirect.start()

        #threading screeShot
        self.threadSC = Thread(target = self.SC.shot)
        self.threadSC.start()

        #start writing
        self.write()
        print("__init__ VW complete")

    def write(self):
        print("start write")
        pic = self.SC.q.get()   
        a = cv2.cvtColor(np.array(pic["pic"]), cv2.COLOR_RGB2BGR)
        self.height, self.width, self.channels = a.shape
        self.out = cv2.VideoWriter(self.outputFile, self.format, self.SC.bitrate, (self.width, self.height))
        self.out.write(a)

        print("Bitrate : ", self.SC.bitrate)
        startTime = time.time() * 100
        nextPic = self.SC.q.get()
        curKey = None
        keys = []
        while self.SC.expression:  # expression  
            self.shotEvent.wait()
            pic = nextPic
            nextPic = self.SC.q.get()
            # if not self.redirect.event.empty():
            #     if curKey == None:
            #         curKey = self.redirect.event.get()
            #     while curKey["time"] < nextPic["time"]:
            #         keys.append(curKey["but"])
            #         curKey = self.redirect.event.get()
            # if len(keys) != 0:
            #     print(keys)
            x, y = pic["position"]
            pic['pic'].paste(self.mouse, (x, y), self.mouse)
            pic = cv2.cvtColor(np.array(pic["pic"]), cv2.COLOR_RGB2BGR)
            self.out.write(pic)
            keys = []
        endTime = time.time() * 100
        print("Work Time : ", endTime - startTime, "sec * 10^-2")
        self.save()

    def stop(self, expession):
        self.SC.expession = expession

    def save(self):
        #self.redirect.kill()
        self.out.release()
        cv2.destroyAllWindows() 
