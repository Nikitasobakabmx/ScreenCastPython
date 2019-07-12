from pynput import mouse


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
            self.pressed.update({'button' : None})

    def on_scroll(self, x, y, dx, dy):
        self.pressed.update({'dy' : dy})

    def start_listen(self):
        with mouse.Listener(
                on_move = self.on_move,
                on_click = self.on_click,
                on_scroll = self.on_scroll) as listener:
            listener.join()


m = MouseClick()
m.start_listen()
