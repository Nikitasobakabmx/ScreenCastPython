import os
from queue import Queue
import pyautogui
import mss
from threading import Thread, Lock, Event
import time
from Redirector import Redirector

class ScreenCatcher:
    def __init__(self, event):
        with mss.mss() as sct:
            print("start SC")
            self.redirect = Redirector()
            self.VWEvent = event
            self.q = Queue()
            self.monitor = sct.monitors[1]
            self.mutex = Lock()

            #count bitrate
            startTime  = time.perf-counter()
            self.q.put({"pic": mss.mss().grab(self.monitor), "time": time.time() * 100, "position": self.redirect.position})
            self.time = time.monotonic_ns() - startTime
            self.bitrate = int(0.95*(10**9/self.time))
            self.time = int((10**9/self.bitrate))

            #dying there
            self.shotFactory(self.bitrate)
            print("stop SC")

    def shotFactory(self, shots):
        self.eventList = []
        for _ in range(shots):
            self.eventList.append(Event())
        self.threadList = []
        for i in range(shots):
            self.threadList.append(Thread(target = self.shot_once, args = (eventList[i-1], eventList[i], self.VWEvent if (i == shot-1) else None)))
        for thread in self.threadList:
            thread.start()


    def stopFactory(self, shots):
        for i in self.threadList:
            i.stop()
            i.join()

    def shot_once(self, previousEvent, nextEvent, queueEvent):
        while True:
            previousEvent.wait(1)
            self.mutex.asacquire()
                        #screenShot                     #mouse position         #list of key
            self.q.put((mss.mss().grab(self.monitor), self.redirect.position, self.redirect.events))
            self.redirect.events = []
            nextEvent.set()
            if queueEvent != None:
                queueEvent.set()
            self.mutex.release()

if __name__ == "__main__":
