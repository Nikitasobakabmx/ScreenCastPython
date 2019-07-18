import os
from queue import Queue
import pyautogui
from threading import Thread
import time
from Redirector import Redirector

class ScreenCatcher:
    def __init__(self):
        print("start SC")
        self.q = Queue()        
        self.expression = True
        print("stop SC")
        self.bitrate = 0
        self.redirect = Redirector()
        self.thread = Thread(target = self.redirect.start())
        self.thread.start()

    def shot(self):
        self.startTime = time.time() * 100
        while (time.time()*100 - self.startTime) < 100:
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100, "position": self.redirect.position if self.redirect.position != None else (0,0)})
        self.bitrate = self.q.qsize()
        self.startTime = time.time() * 100
        while (time.time()*100 - self.startTime) < 1000:
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100, "position": self.redirect.position if self.redirect.position != None else (0,0)})
        endTime = time.time() * 100
        print("Shoting time : ", endTime - self.startTime, " sec * 10^-2")

