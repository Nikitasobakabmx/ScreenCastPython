from pynput import keyboard
import time
#<0.07
class KeyboardClick():

    def __init__(self):
        self.pressed = []
        self.prev_time = time.time()
        self.released = []
    
    def start_listen(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        while self.released:
            for r in self.released:
                if r in self.pressed:
                    self.pressed.remove(r)
                self.released.remove(r)
        # try:
        # self.curr_time = time.time()
        # self.diff_time = self.curr_time-self.prev_time
        # self.prev_time = self.curr_time
        # if self.diff_time > 0.07 or (self.released==key):
        #     self.pressed = []
        if key not in self.pressed:
            self.pressed.append(key)
        

    def on_release(self, key):
        self.released.append(key)
        if key == keyboard.Key.esc:
        # Stop listener
            return False

# c = KeyboardClick()
# c.start_listen()
