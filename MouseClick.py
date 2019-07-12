from pynput import mouse


class MouseClick():

    def __init__(self):
        self.pressed = []
        self.released = []

    def on_move(self, x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    def on_click(self, x, y, button, pressed):
        # try:
        if pressed:
            self.pressed.append(button.name)
        else:
            self.released.append(button.name)
        #print(button.name, '{0} at {1}'.format(
        #    'Pressed' if pressed else 'Released',
        #    (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(self, x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    def start_listen(self):
        with mouse.Listener(
                on_move = self.on_move,
                on_click = self.on_click,
                on_scroll = self.on_scroll) as listener:
            listener.join()


m = MouseClick()
m.start_listen()
