import numpy as np
import cv2
from vision import Vision
from hsvfilter import HsvFilter
from time import time
import d3dshot
import win32gui

#Initialize vision class
vision_Class = Vision(None)

#Initialize trackbar window(DEBUG COLORS)
vision_Class.init_control_gui()

#House HSV Filter
#hsv_filter_House = HsvFilter(0,255,0,45,255,255,255,0,255,0)

#Initialize d3dshot
d = d3dshot.create(capture_output="numpy")

#Get screen width and height
hwnd = win32gui.FindWindow(None, 'Counter-Strike: Global Offensive')
rect = win32gui.GetWindowRect(hwnd)
region = rect[0], rect[1], rect[2], rect[3]

#loop_time = time()
#while True
while True:
    screenshot = d.screenshot(region=region)
    screenshot = screenshot[...,::-1]
    processed_image = vision_Class.apply_hsv_filter(screenshot)
    #screenshot = screenshot[...,::-1]

    #screenshot = wincap.get_screenshot()
    #processed_image = vision_Class.apply_hsv_filter(screenshot)
    #processed_image = vision_Class.apply_hsv_filter(screenshot, hsv_filter_House)

    #print('FPS {}'.format(1 / (time() - loop_time)))
    #loop_time = time()
    #frames.append(screenshot)

    cv2.imshow('asd', processed_image)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
