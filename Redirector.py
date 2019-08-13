from pynput import mouse, keyboard
from threading import Thread
#pattern
#{"but":char, "press" : bool}
class Redirector:
    def __init__(self):
        self.events = []
        self.position = (0,0)
        self.scroll_check = False #like a press in on_click # need for unpress scroll buttom

    def start(self):
        self.listener_m = mouse.Listener(on_click=self.on_click,
                                       on_move=self.on_move,
                                       on_scroll=self.on_scroll)
        self.listener_k = keyboard.Listener(on_press=self.on_press,
                                            on_release=self.on_release)
        self.listener_m.start()
        self.listener_k.start()

    def kill(self):
        self.listener_m.join(1)
        self.listener_m.stop()
        self.listener_k.join(1)
        self.listener_k.stop()
        pass
        #how to terminate thread?


    def on_move(self, x, y):
        self.position = (x, y)

    def on_click(self, x, y, button, pressed):
        if {"but" : str(button), "press" : pressed} not in self.events:            
            self.events.append({"but" : str(button), "press" : pressed})
        self.position = (x, y)

    def on_scroll(self, x, y, dx, dy):
        self.position = (x, y)
        if dy > 0 and {"but" :'Button.MoveDown', "press" : self.scroll_check} not in self.events:
            self.scroll_check = True - self.scroll_check
            self.events.append({"but" :'Button.MoveUp', "press" : self.scroll_check})
        elif dy <= 0 and {"but" :'Button.MoveDown', "press" : self.scroll_check} not in self.events:
            self.scroll_check = True - self.scroll_check
            self.events.append({"but" :'Button.MoveDown', "press" : self.scroll_check})


    def on_press(self, key):
        try:
            if str(key.char) not in self.events:
                self.events.append({"but" : str(key.char), "press" : True})
        except AttributeError:
            if str(key.name) not in self.events:
                self.events.append({"but" : str(key.name), "press" : True})

    def on_release(self, key):
        try:
            if str(key.char) not in self.events:
                self.events.append({"but" : str(key.char), "press" : False})
        except AttributeError:
            if str(key.name) not in self.events:
                self.events.append({"but" : str(key.name), "press" : False})
        
    def __del__(self):
        pass
        self.kill()
        #it is demon?

#test
if __name__ == "__main__":
    mrd = Redirector()
    mrd.start()
    f = open('Keys.txt', 'w')
    try:
        for i in range(1000000):
            f.write(str(mrd.event.get()) + "\n")
            print(str(mrd.event.get()) + "\n")
            
    except KeyboardInterrupt:
        del mrd
    f.close()
