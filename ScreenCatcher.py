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


    def start(self):
        print("start start")
        self.threadShot = Thread(target=self.shot)
        self.threadShot.start()
        time.sleep(1)
        self.bitrate = int(self.q.qsize() - self.q.qsize()/5)  # magic
        print("stop start")

    def shot(self):
        startTime = time.time() * 100
        while (time.time()*100 - startTime) < 500:
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100})
        endTime = time.time() * 100
        print("Shoting time : ", endTime - startTime, " sec * 10^-2")

