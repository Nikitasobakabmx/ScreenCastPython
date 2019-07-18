import os
from queue import Queue
import pyautogui
import mss
from threading import Thread, Lock, Event
import time
from Redirector import Redirector

class ScreenCatcher:
    
    def __init__(self, redirector, shotEvent):
        with mss.mss() as sct:
            print("start SC")
            self.redirect = redirector
            self.shotEvent = shotEvent
            self.q = Queue()        
            self.expression = True
            self.monitor = sct.monitors[1]
            self.mutex = Lock()

            #count bitrate
            startTime  = time.monotonic_ns()
            self.q.put({"pic": mss.mss().grab(self.monitor), "time": time.time() * 100, "position": self.redirect.position})
            self.time = time.monotonic_ns() - startTime
            self.bitrate = int(0.95*(10**9/self.time))
            self.time = int((10**9/self.bitrate))
            self.shot_many()
            print("stop SC")


    def shot(self):
        print("start Shot")
        loses = []
        startTime = time.time() * 100
        while (time.time()*100 -  startTime) < 3000:
            curStartTime = time.monotonic_ns()
            self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100, "position": self.redirect.position})
            curTime = time.monotonic_ns() - curStartTime
            if (self.time - curTime) > 0:
                time.sleep((self.time - curTime)/10**9)
                self.shotEvent.set()
            else:
                loses.append(self.time - curTime)
        endTime = time.time() * 100
        print("Shoting time : ", endTime - startTime, " sec * 10^-2")
        print(loses)

    def shotFactory(self):


    def shot_once(self, previousEvent, nextEvent, queueEvent, time):
        self.queueEvent = queueEvent
        self.time = 1 - time
        while True:
            try:
                previousEvent.wait(1)
                mutex.asacquire()
                self.q.put({"pic": mss.mss().grab(self.monitor), "time": time.time() * 100, "position": self.redirect.position})
                nextEvent.set()
                queueEvent.set()
                mutex.release()
            except

