from pynput import mouse


class MouseClick():

    def __init__(self):
        pass

    def start_listen(self):
        with mouse.Listener(
                on_click=self.on_click) as listener:
            listener.join()

    def on_click(self, x, y, button, pressed):
        # try:
        self.pressed = []
        self.pressed.append(button.name)
        if button == mouse.Button.left:
            return 1
        elif button == mouse.Button.right:
            return 2
        else:
            return False


m = MouseClick()
m.start_listen()
