from pynput import mouse, keyboard
from queue import Queue
from copy import deepcopy
from time import time, sleep
from threading import Thread
#{"but": but, "pos":(x, y), "press": bool,"keyBoard": key , "time":time}
class Redirector:
    def __init__(self):
        self.event = Queue()
        self.position = None
    def start(self):
        self.listener_m = mouse.Listener(on_click=self.on_click,
                                       on_move=self.on_move,
                                       on_scroll=self.on_scroll)
        self.listener_k = keyboard.Listener(on_press=self.on_press,
                                            on_release=self.on_release)
        self.listener_m.start()
        self.listener_k.start()

    def kill(self):
        self.listener_m.stop()
        self.listener_m.join()
        self.listener_k.stop()
        self.listener_k.join()

    def on_move(self, x, y):
        self.position = (x, y)

    def on_click(self, x, y, button, pressed):
        self.event.put({"but": button, "time": time()})
        self.position = (x, y)

    def on_scroll(self, x, y, dx, dy):
        self.position = (x, y)
        self.event.put({"but": "MoveUp" if dy > 0 else "MoveDown", "time": time()})
    def on_press(self, key):
        try:
            self.event.put({"but": key.char, "time": time()})
        except AttributeError:
            self.event.put({"but": key.name, "time": time()})

    def on_release(self, key):
        try:
            self.event.put({"but": key.char, "time": time()})
        except AttributeError:
            self.event.put({"but": key.name, "time": time()})
        
    def __del__(self):
        self.kill()
if __name__ == "__main__":
    mrd = Redirector()
    mrd.start()
    f = open('NoKeys.txt', 'w')
    try:
        for _ in range(10):
            f.write(str(mrd.event.get()) + "\n")
            print(str(mrd.event.get()) + "\n")
    except KeyboardInterrupt:
        del mrd
    f.close()
