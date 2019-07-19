from pynput import mouse, keyboard
from queue import Queue
from copy import deepcopy
from time import time, sleep
from threading import Thread
#{"but": but, "pos":(x, y), "press": bool,"keyBoard": key , "time":time}
class Redirector:
    def __init__(self):
        self.event = Queue()
        self.events = []
        self.position = (0,0)
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
        if button not in self.events:            
            self.events.append(button)
        self.position = (x, y)

    def on_scroll(self, x, y, dx, dy):
        self.position = (x, y)
        if dy > 0 and 'MoveUp' not in self.events:
            self.events.append('MoveUp')
        elif dy <= 0 and 'MoveUp' not in self.events:
            self.events.append('MoveUp')
        #self.event.put({"but": "MoveUp" if dy > 0 else "MoveDown", "time": time()})

    def on_press(self, key):
        try:
            if key.char not in self.events:
                self.events.append(key.char)
        except AttributeError:
            if key.name not in self.events:
                self.events.append(key.name)
        #self.event.put({"but": key.name, "time": time()})

    def on_release(self, key):
        try:
            print('yos')
            self.events.remove(key.char)
        except AttributeError:
            self.events.remove(key.name)
        
    def __del__(self):
        self.kill()
if __name__ == "__main__":
    mrd = Redirector()
    mrd.start()
    f = open('NoKeys.txt', 'w')
    try:
        for _ in range(1000000):
            f.write(str(mrd.events) + "\n")
            print(str(mrd.events) + "\n")
    except KeyboardInterrupt:
        del mrd
    f.close()
