from ScreenCatcher import ScreenCatcher
from VideoWriter import VideoWriter
from threading import Thread

def inpt(vW):
    a = input("Want to stop?")
    vW.stop(a)
    

if __name__ == "__main__":
    vW = VideoWriter()