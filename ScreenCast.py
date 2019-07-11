import threading

class ScreenCast:
    def __init__(self):
        self.mouseThred = threading.Thread(target = self.mouseClick)
        self.keybordThred = threading.Thread(target = self.keybordClick)
        self.screenThred = threading.Thread(target = self.screenCatcher)
        self.videoWriterThred = threading.Thread(target = self.videoWriter)
    def mouseClick(self):
        pass
    def keybordClick(self):
        pass
    def screenCatcher(self):
        pass
    def videoWriter(self):
        pass