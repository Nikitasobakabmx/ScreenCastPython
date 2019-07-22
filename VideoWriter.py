import cv2
from numpy import array
from threading import Thread, Event
from time import perf_counter
from ScreenCatcher import ScreenCatcher
from Redirector import Redirector
from copy import deepcopy
from time import perf_counter
try:
    import Image, ImageDraw, ImageFont
except ImportError:
    from PIL import Image, ImageDraw, ImageFont
from PIL import ImageDraw, ImageFont

class VideoWriter:
    
    def __init__(self, outputFile="video.avi", format="mp4v"):
        self.mouse = Image.open("Images/Mouse/mouse.png")
        self.outputFile = outputFile
        self.format = cv2.VideoWriter_fourcc(*format)
        
        self.keyList = {}
        f = open("key.txt", "r")
        for line in f:
            ln = line.split(" ")
            self.keyList[ln[0]] = ln[1] 
        f.close()

        self.ev = Event()
        
        self.SC = ScreenCatcher(self.ev)

        self.WriteProcess = Thread(target=self.write)
        self.WriteProcess.start()
        
        self.out = cv2.VideoWriter(self.outputFile, self.format, self.SC.bitrate, (self.SC.width, self.SC.height))

    def write(self):
        self.ev.wait(1)
        queue = self.SC.q.get()
        start_time = perf_counter() * 100
        buffer = []
        while perf_counter() * 100 - start_time < 1000:  # expression
            startTime = perf_counter() * 100
            self.ev.wait(1)
            self.ev.clear()
            queue = self.SC.q.get()
            queue[0] = Image.frombytes("RGB", queue[0].size, queue[0].bgra, "raw", "BGRX")
            x_mouse, y_mouse = queue[1]
            ImgSize = 0
            keys = queue[2]
            while keys != []:
                #keyboard
                if keys[0][0] != 'B':
                    queue[0].paste(self.mouse, (x_mouse, y_mouse), self.mouse)
                    buffer.append({"key" : keys[0], "time" : perf_counter()})
                #mouse
                else:
                    img = Image.open("Images/Mouse/{}.png".format(keys[0]))
                    queue[0].paste(img, (x_mouse, y_mouse), img)
                keys.pop(0)
            else:
                queue[0].paste(self.mouse, (x_mouse, y_mouse), self.mouse)
            for i in buffer:
                if perf_counter() - i["time"] > 1:
                    buffer.remove(i)
                else:
                    x, y = (25 + ImgSize), int(0.75 * self.SC.height)
                    try:
                        img = Image.open("Images/Keyboard/{}.png".format(self.keyList[i["key"]]))
                    except FileNotFoundError:
                        img = Image.open("Images/Keyboard/Template.png")
                        draw = ImageDraw.Draw(img)
                        font = ImageFont.truetype("Images/Keyboard/Times_New_Roman.ttf", 30)
                        draw.text((60, 55), str(i["key"]),(0, 0, 0),font=font)
                        img.save('Images/Keyboard/{}.png'.format(str(i["key"])))
                        self.keyList[i["key"]] = "Images/Keyboard/" + str(i["key"]) + ".png"
                        img = Image.open("{}".format(self.keyList[i["key"]]))
                    ImgSize += 160
                    queue[0].paste(img, (x, y), img)
            queue[0] = cv2.cvtColor(array(queue[0]), cv2.COLOR_RGB2BGR)
            self.out.write(queue[0])
        endTime = perf_counter() * 100
        print("Work Time : ", endTime - start_time, "sec * 10^-2")
        print(self.SC.bitrate)
        self.SC.stopFactory(self.SC.shots)
        #self.redirect.kill()
        self.save()

    def stop(self, expession):
        self.SC.expession = expession
        f = open("key.txt", "w")
        for i in keyList.items():
            f.write(str(i[0]) + " " + str(i[1]))
        f.close()

    def save(self):
        #self.redirect.kill()
        self.out.release()
        cv2.destroyAllWindows()
