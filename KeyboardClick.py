from pynput import keyboard

class KeyboardClick():

    def __init__(self):
        pass
    
    def start_listen(self):
        with keyboard.Listener(
            on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        # try:
        self.pressed = []
        self.pressed.append(key)
        if key == keyboard.Key.esc:
            return False

    def on_release(self, key):
        print('{0} released'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

c = KeyboardClick()
c.start_listen()

# Collect events until released
# with keyboard.Listener(
#         on_press=c.on_press) as listener:
#     listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press)
# listener.start()
