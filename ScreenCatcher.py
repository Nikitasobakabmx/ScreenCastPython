import os
from queue import Queue
import pyautogui
from threading import Thread
import time

class ScreenCatcher:
    def __init__(self):
        print("start SC")
        self.q = Queue()
        self.start()        
        self.expression = True
        print("stop SC")
        self.bitrate = 0

    def start(self):
        print("start start")
        self.threadShot = Thread(target=self.shot)
        self.threadShot.start()
        print("stop start")

    def shot(self):
        self.startTime = time.time() * 100
        while (time.time()*100 - self.startTime) < 100:
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100})
        self.bitrate = self.q.qsize()
        self.startTime = time.time() * 100
        while (time.time()*100 - self.startTime) < 500:
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100})
        endTime = time.time() * 100
        print("Shoting time : ", endTime - self.startTime, " sec * 10^-2")

