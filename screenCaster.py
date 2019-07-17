from multiprocessing import Process, Queue
import time
import mss
import mss.tools


def grab(queue):
    # type: (Queue) -> None

    rect = {"top": 0, "left": 0, "width": 1600 , "height": 900}

    with mss.mss() as sct:
        startTime = time.time()*100
        while (time.time()*100 - startTime) < 100:
            queue.put(sct.grab(rect))
    print("FPS : ", queue.qsize())

def save(queue):
    # type: (Queue) -> None

    number = 0
    output = "screenshots/file_{}.png"
    to_png = mss.tools.to_png

    while "there are screenshots":
        img = queue.get()
        if img is None:
            break

        to_png(img.rgb, img.size, output=output.format(number))
        number += 1


if __name__ == "__main__":
    # The screenshots queue
    queue = Queue()  # type: Queue

    # 2 processes: one for grabing and one for saving PNG files
    Process(target=grab, args=(queue,)).start()
    #Process(target=save, args=(queue,)).start()