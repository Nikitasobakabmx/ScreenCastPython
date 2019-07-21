import os
from queue import Queue
# import pyautogui
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
            #self.mutex = Lock()

            #count bitrate
            startTime  = time.monotonic_ns()
            self.q.put({"pic": mss.mss().grab(self.monitor), "time": time.time() * 100, "position": self.redirect.position})
            self.shotTime = time.monotonic_ns() - startTime
            self.bitrate = int(0.90*(10**9/self.shotTime))
            self.shotTime = int((10**9/self.bitrate))

            self.shotFactory()
            print("stop SC")


    # def shot(self):
    #     print("start Shot")
    #     loses = []
    #     startTime = time.time() * 100
    #     while (time.time()*100 -  startTime) < 3000:
    #         curStartTime = time.monotonic_ns()
    #         self.q.put({"pic": pyautogui.screenshot(), "time": time.time() * 100, "position": self.redirect.position})
    #         curTime = time.monotonic_ns() - curStartTime
    #         if (self.time - curTime) > 0:
    #             time.sleep((self.time - curTime)/10**9)
    #             self.shotEvent.set()
    #         else:
    #             loses.append(self.time - curTime)

    #     endTime = time.time() * 100
    #     print("Shoting time : ", endTime - self.startTime, " sec * 10^-2")

    def shotFactory(self):
        nextEvent = Event()
        previousEvent = Event()
        #count time of create Thraed
        startTime = time.monotonic_ns()
        threadOne = Thread(target = self.shot_once, args = (previousEvent, nextEvent, self.shotEvent, self.shotTime, self.redirect))
        endTime = time.monotonic_ns() - startTime

        threadTwo = Thread(target = self.shot_once, args = (nextEvent, previousEvent, self.shotEvent, self.shotTime, self.redirect))
        threadOne.start()
        time.sleep(self.shotTime - endTime)
        threadTwo.start()

    def shot_once(self, previousEvent, nextEvent, queueEvent, shotTime, redirect):
        self.queueEvent = queueEvent
        #local = 1.0 - time
        while True:
            previousEvent.wait(1)
            #self.mutex.asacquire()
            self.q.put({"pic": mss.mss().grab(self.monitor), "time": time.time() * 100, "position": redirect.position})
            nextEvent.set()
            queueEvent.set()
            #mutex.release()

if __name__ == "__main__":
    redirect = Redirector()
    thread = Thread(target = redirect.start)
    ev = Event()
    test = ScreenCatcher(redirect, ev)
