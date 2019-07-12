from pynput import mouse
import time


class MouseClick():

    def __init__(self):
        self.pressed = {'button' : None, 'x' : None, 'y' : None, 'dy' : None}

    def on_move(self, x, y):
        self.pressed.update({'x' : x, 'y' : y})

    def on_click(self, x, y, button, pressed):
        # try:
        if pressed:
            self.pressed.update({'button' : button.name})
        if not pressed:
            self.pressed.update({'button': None})

    def on_scroll(self, x, y, dx, dy):
        self.pressed.update({'dy' : dy})

    def start_listen(self):
        listener = mouse.Listener(
                on_move = self.on_move,
                on_click = self.on_click,
                on_scroll = self.on_scroll)
        listener.start()
        try:
            listener.wait()
        finally:
            listener.stop()
            return self.pressed


m = MouseClick()
for i in range(10000000000000):
    print(m.start_listen())
