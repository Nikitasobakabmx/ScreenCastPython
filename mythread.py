import threading
import time

A = 0
A_MUTEX = threading.Lock()

E = threading.Event()

def thread_factory(i):
    def my_thread():
        if i == 2:
            E.wait()
        for _ in range(1000):
            global A
            with A_MUTEX:
                print("Thread", i, "is running:", A)
        if i == 1:
            E.set()
        return 0
    return my_thread

t1 = threading.Thread(target=thread_factory(1))
t2 = threading.Thread(target=thread_factory(2))
t1.start()
t2.start()
t1.join()
t2.join()
