import cv2
from numpy import array
from threading import Thread, Event
from ScreenCatcher import ScreenCatcher
from time import perf_counter

try:
    import Image, ImageDraw, ImageFont
except ImportError:
    from PIL import Image, ImageDraw, ImageFont


class VideoWriter:

    def __init__(self, outputFile="video1.avi", format="mp4v"):
        self.mouse = Image.open("Images\\Mouse\\mouse.png")
        self.outputFile = outputFile
        self.format = cv2.VideoWriter_fourcc(*format)

        self.keyList = {}
        self.keyListStatus = {}
        f = open("key.txt", "r")
        for line in f:
            ln = line.split(" ")
            self.keyList[ln[0]] = ln[1][:-1]
            self.keyListStatus[ln[0]] = False

        f.close()
        self.expression = True

        self.ev = Event()

        self.SC = ScreenCatcher(self.ev)
        self.SC.shotFactory()

        self.out = cv2.VideoWriter(self.outputFile, self.format, self.SC.bitrate, (self.SC.width, self.SC.height))
        
        self.cursore_path = "Images\\Mouse\\mouse.png"
        self.cursor = Image.open(self.cursore_path)
        self.cursor = array(self.cursor)
        self.mouse_back_path = "Images\\Mouse\\Button.Empty.png"
        self.mouse_state = {"Button.left" : False,
                            "Button.right" : False, 
                            "Button.middle" : False, 
                            "Button.MoveUp" : False, 
                            "Button.MoveDown" : False}
        self.mouse_background = Image.open(self.mouse_back_path)
        self.mouse_path = "Images\\Mouse\\"
        self.mouse_position = (self.SC.width - 25 - self.mouse_background.size[0], self.SC.height - 25 - self.mouse_background.size[1])

    def run(self):
        self.WriteProcess = Thread(target=self.write)
        self.WriteProcess.start()

    def write(self):
        self.ev.wait(1)
        queue = self.SC.q.get()
        start_time = perf_counter() * 100
        
        while self.expression:  # expression
            startTime = perf_counter() * 100
            self.ev.wait(1)
            self.ev.clear()
            queue = self.SC.q.get()
            queue[0] = array(queue[0])
            queue[0] = self._write_interface(queue[0], queue[2], queue[1])
            # queue[0] = queue[0].resize((int(queue[0].size[0] * 0.5),
            #                         int(queue[0].size[1] * 0.5)),
            #                         Image.ANTIALIAS)
            queue[0] = cv2.cvtColor(array(queue[0]), cv2.COLOR_RGB2BGR)
            self.out.write(queue[0])
        endTime = perf_counter() * 100
        print("Work Time : ", endTime - start_time, "sec * 10^-2")
        print(self.SC.bitrate)
        self.SC.stopFactory()
        self.save()





    def _write_interface(self, img, keys, position): #image now is nympy array
        ImgSize = 0
        #paste cursor
        width = len(img)
        higth = len(img[0])
        for i in range(len())
        x, y = 0, 0
        for key in keys[::-1]:
            # keyboard # if name start with 'B' this is Button... # on keyboards only keys
            if key["but"][0] != 'B':
                self.keyListStatus[key["but"]] = key["press"]
            # mouse
            else:
                self.mouse_state[key["but"]] = key["press"]
        for key, val in self.mouse_state.items():
            if val:
                mouse_img = Image.open(self.mouse_path + key + ".png")
                self.mouse_background.paste(mouse_img, (0, 0), mouse_img)

        for key, val in self.keyListStatus.items():
            if val:
                x, y = (25 + ImgSize), int(0.75 * self.SC.height)
                try:
                    keyImg = Image.open("Images\\Keyboard\\" + str(self.keyList[key]) + ".png")
                except FileNotFoundError:
                    keyImg = Image.open("Images\\Keyboard\\Template.png")
                    draw = ImageDraw.Draw(keyImg)
                    font = ImageFont.truetype("Images\\Keyboard\\Times_New_Roman.ttf", 20)
                    draw.text((50 - len(str(key)) * 4, 45), str(key), (0, 0, 0), font=font)
                    keyImg.save('Images\\Keyboard\\' + (str(key)) + ".png")
                    self.keyList[key] = "Images\\Keyboard\\" + str(key) + ".png"
                    keyImg = Image.open(self.keyList[key])
                ImgSize += 160
                img.paste(keyImg, (x, y), keyImg)
        self.mouse_background = self.mouse_background.resize((int(self.mouse_background.size[0] * 0.2), int(self.mouse_background.size[1] * 0.2)), Image.ANTIALIAS)
        img.paste(self.mouse_background, self.mouse_position, self.mouse_background)
        self.mouse_background = Image.open(self.mouse_back_path)
        return img
    def stop(self):
        self.expression = False
        self.WriteProcess.join()
        f = open("key.txt", "w")
        for i in self.keyList.items():
            f.write(str(i[0]) + " " + str(i[1]) + "\n")
        f.close()

    def save(self):
        self.redirect.kill()
        self.out.release()
        cv2.destroyAllWindows()
