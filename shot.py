import cv2
import os
from multiprocessing import Process, Queue
import numpy as np
import pyautogui
from PIL import Image
from pynput import keyboard, mouse
import time

def funcShot(q):
    while True: #(time.time()*100 - startTime) < 95:
        a = pyautogui.screenshot()
        q.put({"pic" : a, "time" : time.time()*100})


if __name__ == "__main__":
    q = Queue(100)
    print("start!")
    
    threadOne = Process(target = funcShot, args = (q, ))
    threadTwo = Process(target = funcShot, args = (q, ))
    threadThree = Process(target = funcShot, args = (q, ))
    threadFour = Process(target = funcShot, args = (q, ))
    
    #q.close()
    #q.join_thread()
    threadTwo.start()
    threadOne.start()
    threadThree.start()
    threadFour.start()
    time.sleep(1)
    size = int(q.qsize() - q.qsize()/15)
    #threadOne.join()
    #threadTwo.join()
    #threadThree.join()
    #threadFour.join()
    a = []
    print("work")
    format = cv2.VideoWriter_fourcc(*"mp4v")
    a = pyautogui.screenshot()
    a = cv2.cvtColor(np.array(a), cv2.COLOR_RGB2BGR)
    high, weight, glub = a.shape
    out = cv2.VideoWriter("video.avi", format, size, (weight,high))
    startTime = time.time() * 100
    while time.time() * 100 - startTime < 500:
        print("Work!")
        a = q.get()
        pic = cv2.cvtColor(np.array(a["pic"]), cv2.COLOR_RGB2BGR)
        out.write(pic)
    print(time.time() * 100 - startTime)
    out.release()
    cv2.destroyAllWindows()
    threadTwo.terminate()
    threadOne.terminate()
    threadThree.terminate()
    threadFour.terminate()

    print("complete!")
    #threadOne.join()
    #threadTwo.join()
    #threadThree.join()
    #threadFour.join()
    #stopTime = time.time()*100 - startTime
    #print("Общее время :", stopTime)
    #print(q.qsize())
    #print(len(s))