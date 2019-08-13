import mss
import time
from threading import Thread
from queue import  Queue

def make_shot(queue, monitor):
    while True:
        with mss.mss() as sct:
            queue.put(sct.grab(monitor))


if __name__ == "__main__":
    queue = Queue()
    monitor = {"width" : 1600, "height" : 900}
    with mss.mss() as sct:
        monitor = sct.monitors[1]
    thread_one = Thread(target = make_shot, args = (queue, monitor))
    thread_one.start()
    thread_Two = Thread(target = make_shot, args = (queue, monitor))
    thread_Two.start()
    thread_Three = Thread(target = make_shot, args = (queue, monitor))
    thread_Three.start()
    time.sleep(1)
    print(queue.qsize())
    thread_one.join()
    thread_one.stop()
    thread_Two.join()
    thread_Two.stop()
    thread_Three.join()
    thread_Three.stop()
    queue.join()
    queue.stop()