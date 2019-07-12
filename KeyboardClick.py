from pynput import keyboard

class KeyboardClick():

    def __init__(self):
        self.pressed = []
        self.released = []
        self.stop = False
    
    



    def on_press(self, key):
        
        # while self.released:
        #     for r in self.released:
        #         if r in self.pressed:
        #             self.pressed.remove(r)
        #         self.released.remove(r)
        # if key not in self.pressed:
        print('key', key)
        self.pressed.append(key)
        #print(self.pressed)
        

    def on_release(self, key):
        self.released.append(key)
        # if key == keyboard.Key.esc:
        #  # Stop listener
        #     self.stop_listen()

    def start_listen(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        print('start')
        listener.start()
        try:
            print('try')
            listener.wait()
        finally:
            listener.stop()
            #print(self.pressed)b bfdsf
            return self.pressed

c = KeyboardClick()
for i in range(100000):
    print(c.start_listen())
# c.stop_listen()
