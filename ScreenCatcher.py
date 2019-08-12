from queue import Queue
import mss
from threading import Thread, Lock, Event
import time
from Redirector import Redirector

class ScreenCatcher:
    def __init__(self, event):
        with mss.mss() as sct:
            self.redirect = Redirector()
            redirectThread = Thread(target = self.redirect.start())

            self.VWEvent = event
            self.q = Queue()
            self.mutex = Lock()
            
            self.monitor = sct.monitors[1]
            self.width = self.monitor["width"]
            self.height = self.monitor["height"]
            self.shots = 2
            self.expression = True

            #count bitrate
            startTime  = time.perf_counter_ns()
            self.q.put([sct.grab(self.monitor),self.redirect.position, self.redirect.events])
            self.redirect.events = []
            self.time = time.perf_counter_ns() - startTime
            self.bitrate = int(0.9*(10**9/self.time))
            self.time = int((10**9/self.bitrate))

    def shotFactory(self):
        self.eventList = []
        for _ in range(self.shots):
            self.eventList.append(Event())
        self.threadList = []
        for i in range(self.shots):
            self.threadList.append(Thread(target = self.shot_once,
                                    args = (self.eventList[i-1],
                                    self.eventList[i],
                                    self.VWEvent,# if (i == shots-1) else None, 
                                    i))) 
        self.eventList[-1].set()
        for thread in self.threadList:
            thread.start()


    def stopFactory(self):
        # for i in self.threadList:
        #     i.join(1)
        self.expression = False
        self.redirect.kill()

    def shot_once(self, previousEvent, nextEvent, queueEvent, count):
        next_time = time.perf_counter_ns()
        while self.expression:
            with mss.mss() as sct:
                previousEvent.wait()

                self.mutex.acquire()
                next_time += self.time
                previousEvent.clear()
                start_time = time.perf_counter_ns()
                            #screenShot                     #mouse position         #list of key
                self.q.put([sct.grab(self.monitor), self.redirect.position, self.redirect.events])
                self.redirect.events = []
                self.mutex.release()
                
                end_time = (time.perf_counter_ns() - start_time) / 10**9
                time.sleep((self.time/10**9 - end_time - ((next_time/10**9) % 0.015)) if (self.time/10**9 - end_time - ((next_time/10**9) % 0.015)) > 0 else 0 )
                while time.perf_counter_ns() < next_time:
                     pass
                if queueEvent != None: 
                    queueEvent.set()    
                nextEvent.set()
#test
if __name__ == "__main__":
    ec = Event()
    sc = ScreenCatcher(ec)