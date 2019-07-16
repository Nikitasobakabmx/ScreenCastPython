from multiprocessing import Process, Queue
import cv2
import mss
import mss.tools
import time


def grab(queue, num):
    # type: (Queue) -> None
    for _ in range(5):

        rect = {"top": 0, "left": 0, "width": 1600, "height": 900}
        a =  []
        with mss.mss() as sct:
            startTime = time.time() * 100
            while (time.time() * 100 - startTime) < 100:
                a.append((sct.grab(sct.monitors[1]), time.time()))
        print("Process ", num, " : ", len(a))
        queue.put(a)

def save_to_file(queue):
    arr = []
    key = True
    out = None
    format = cv2.VideoWriter_fourcc(*"mp4v")
    try:
        while not queue.empty():
            if not queue.empty():
                for a in queue.get():
                    arr += a
                arr.sorted(key = lambda X : X[1])
                

                for a in arr:
                    a =  cv2.cvtColor(np.array(a[0]), cv2.COLOR_RGB2BGR)
                    if key :
                        key = False
                        height, width, channels = a.shape
                        out = cv2.VideoWriter("video40.avi", format, 32.5, (width, height))
                    out.write(a)
    except KeyboardInterrupt:
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # The screenshots queue
    queue = Queue()  # type: Queue
    length = []
    # 2 processes: one for grabing and one for saving PNG files
    for i in range(4):
        length.append(Process(target=grab, args=(queue, i)))
        length[-1].start()
    try:
        save_to_file(queue)
    except KeyboardInterrupt:
        pass

    for a in length:
        a.kill()
