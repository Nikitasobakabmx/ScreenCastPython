from pynput import mouse, keyboard
from queue import Queue
from copy import deepcopy
from time import time, sleep
from threading import Thread
#{"but": but, "pos":(x, y), "press": bool,"keyBoard": key , "time":time}
class Redirector:
    def __init__(self):
        pass
    def start(self):
        self.event = Queue()
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
        pass

    def on_click(self, x, y, button, pressed):
        self.event.put({"but": button, "keyBoard": None, "time": time()})

    def on_scroll(self, x, y, dx, dy):
        self.event.put({"but": "MoveUp" if dy > 0 else "MoveDown", "keyBoard": None, "time": time()})

    def on_press(self, key):
        try:
            self.event.put({"but": None, "keyBoard": key.char, "time": time()})
        except AttributeError:
            self.event.put({"but": None, "keyBoard": key, "time": time()})

    def on_release(self, key):
        pass
        # try:
        #     self.event.put({"but": None, "pos": None, "press": False, "keyBoard": key.char, "time": time()})
        # except AttributeError:
        #     self.event.put({"but": None, "pos": None, "press": False, "keyBoard": key, "time": time()})
    def __del__(self):
        self.kill

mrd = Redirector()
f = open('keys.txt', 'w')
try:
    while True:
        f.write(str(mrd.event.get()) + "\n")
except KeyboardInterrupt:
    del mrd
f.close()