from pynput import mouse, keyboard
from queue import Queue
from copy import deepcopy
from time import time, sleep

class Redirector:
    def __init__(self, on_click, on_scroll, on_move):
        self.queue = Queue()
        self.should_work = True
        self.frequency = 60

        def ev_redirector(to):
            def event_wrapper(*a, **kw):
                self.queue.put({'to': to, 'a': deepcopy(a), 'kw': deepcopy(kw)})
                return self.should_work
            return event_wrapper
        self.listener_m = mouse.Listener(on_click=ev_redirector(on_click),
                                       on_move=ev_redirector(on_move),
                                       on_scroll=ev_redirector(on_scroll))
        self.listener_k = keyboard.Listener(on_press=ev_redirector(on_press),
                                            on_release=ev_redirector(on_release))
        self.listener_m.start()
        self.listener_k.start()

    def fire_events(self):
        while not self.queue.empty():
            event = []
            nowait = self.queue.get_nowait()['a']
            try:
                if isinstance(nowait[3], bool):
                    event.append([nowait[2].name, nowait[0], nowait[1], nowait[3], None, time()])
                else:
                    if nowait[3] > 0:
                        event.append(["up", nowait[0], nowait[1], True, None, time()])
                    else:
                        event.append(["down", nowait[0], nowait[1], True, None, time()])
            except IndexError:
                if len(nowait) == 1:
                    if isinstance(nowait[0], keyboard._win32.KeyCode):
                        event.append([None, None, None, None, nowait[0], time()])
                    else:
                        event.append([None, None, None, None, nowait[0].name, time()])
            return(event)

    def kill(self):
        self.should_work = False
        self.listener_m.stop()
        self.listener_m.join()
        self.listener_k.stop()
        self.listener_k.join()

def on_move(x, y):
    return

def on_click(x, y, button, pressed):
    pass
    #print('{0} at {1}'.format(
    #    'Pressed' if pressed else 'Released',
    #    (x, y)))

def on_scroll(x, y, dx, dy):
    pass
    #print('Scrolled {0} at {1}'.format(
    #    'down' if dy < 0 else 'up',
    #    (x, y)))

def on_press(key):
    pass
    #print('alphanumeric key {0} pressed'.format(
    #       key.char))

def on_release(key):
    pass
    #print('{0} released'.format(
    #    key))

mrd = Redirector(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
mrd.frequency = 11
for _ in range(10000):
    sleep(0.01)
    print(mrd.fire_events())

mrd.kill()