import numpy as np
import os
import pyautogui

class ScreenCatcher:
    def __init__(self):
        self.img = []
        self.img.append(pyautogui.screenshot())
    
    def shot(self):
        while True:
            self.img.append(pyautogui.screenshot())
    