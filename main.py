from VideoWriter import VideoWriter
    
espression = True

if __name__ == "__main__":
    vW = VideoWriter()
    vW.run()
    while True:
        tmp = input()
        if tmp == "quit":
            break
    vW.stop()