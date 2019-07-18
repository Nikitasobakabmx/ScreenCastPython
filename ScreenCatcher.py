import os
from queue import Queue
import pyautogui
from threading import Thread
import time
from Redirector import Redirector

class ScreenCatcher:
    def __init__(self, redirector):
        print("start SC")
        self.redirect = redirector
        self.q = Queue()        
        self.expression = True
        

        #count bitrate
        startTime  = time.monotonic_ns()
        self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100, "position": self.redirect.position})
        self.time = time.monotonic_ns() - startTime
        self.bitrate = int(0.88*(10**9/self.time))
        
        print("stop SC")


    def shot(self):
        print("start Shot")
        loses = []
        startTime = time.time() * 100
        while (time.time()*100 - startTime) < 3000:
            curStartTime = time.monotonic_ns()
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100, "position": self.redirect.position})
            curTime = time.monotonic_ns() - curStartTime
            if (self.time - curTime) > 0:
                time.sleep((self.time - curTime)/10**9)
            else:
                loses.append(self.time - curTime)
        endTime = time.time() * 100
        print("Shoting time : ", endTime - startTime, " sec * 10^-2")
        print(loses)

