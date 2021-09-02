import win32api
import time
import os

mouse_Movement_Folder = "C:\\Users\\Omistaja\\Desktop\\TurnMouse\\mousemovements\\"

def mouse_cap(length):
    state_v_key = win32api.GetKeyState(0x56) # v button down

    while True:
        #State of v key
        v = win32api.GetKeyState(0x56)

        #Gets x,y of cursor position
        x, y = win32api.GetCursorPos()
        print(x,y)
                
        if v != state_v_key:  # Button state changed
            state_v_key = v
            if v < 0:
                print("v Button Pressed")
                break
        #writes the values into a notepad  
        with open(mouse_Movement_Folder + "\\" + str(length) + ".txt", "a") as f:
            f.write(str(x) + "," + str(y) + "\n")

def record_macros():
    #Press button g to start recording the macro
    state_c_key = win32api.GetKeyState(0x43)
    while True:
        #Gets key state of g key
        c = win32api.GetKeyState(0x43)
        #Gets current mouse position
        c_key_pressed = 0
        if c != state_c_key:  # Button state changed
            if c < 0:
                c_key_pressed = 1
                if c_key_pressed == 1:
                    mouse_cap(len(os.listdir(mouse_Movement_Folder)))

record_macros()
