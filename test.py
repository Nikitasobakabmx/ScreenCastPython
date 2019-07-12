import cv2
import threading
import numpy as np
import pyautogui

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

class ScreenCatcher:
    def __init__(self):
        self.img = pyautogui.screenshot()
    def shot(self):
        img = pyautogui.screenshot()
        return img
class VideoWriter:
    
    def __init__(self, output = "video.avi", format = "mp4v"):

        self.SC = ScreenCatcher()
        self.start(output, format)

        self.SC.shot()
        self.write()

    def write(self):
        try:
            while True:
                img = cv2.cvtColor(np.array(self.SC.shot()), cv2.COLOR_RGB2BGR)
                self.out.write(img)
        except KeyboardInterrupt:
            self.save()

    def save(self):
        self.flag = False
        self.out.release()
        cv2.destroyAllWindows()
    def start(self, output = "video.avi", format = "mp4v"):
        self.flag = True
        self.output = output
        self.format = cv2.VideoWriter_fourcc(*format)
        self.SC.img[0] = cv2.cvtColor(np.array(self.SC.img[0]), cv2.COLOR_RGB2BGR)
        self.height, self.width, self.channels = self.SC.img[0].shape
        self.out = cv2.VideoWriter(self.output, self.format, 20.0, (self.width, self.height))

if __name__ == "__main__":
    
    vW = VideoWriter()
    vW.write()
    vW.save()