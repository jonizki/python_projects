import os
import time

dir = "C:\\Users\\Omistaja\\Desktop\\TurnMouse\\mousemovementfolder\\"


for i in range(941):
    os.mkdir(dir + str(i))
    time.sleep(0.05)
