from KeyboardClick import KeyboardClick

import threading
import time

kb = KeyboardClick()

def thread_factory():
    def my_thread():
        kb.start_listen()
        for _ in range(1000):
            print("buttons", kb.pressed, "pressed")
        return 0
    return my_thread

t1 = threading.Thread(target=thread_factory())
t1.start()
t1.join()
