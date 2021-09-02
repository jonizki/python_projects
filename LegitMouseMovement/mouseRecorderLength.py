import win32api
import time
import os
import datetime
import math

mouse_Movement_Folder = "C:\\Users\\Omistaja\\Desktop\\BOTPROJECT\\MoveCursor\\mousemovements\\"

def delete_File(file):
    #Wait until file appears in folder
    time.sleep(0.6)
    #Delete file
    os.remove(file)

def mouse_cap(length, movement_length):
    counter = 0
    x_orig = 0
    y_orig = 0

    #Used to calculate length of mouse movement
    prev_Hypotenuse_Length = 0

    #Movement changed direction
    direction = 0
    
    while True:
        #Gets x,y of cursor position
        x, y = win32api.GetCursorPos()
        #print(x,y)
        
        if counter == 0:
            x_orig = x
            y_orig = y
            counter += 1

        A = abs(x_orig-x)
        B = abs(y_orig-y)
    
        #calculate hypotenuse length
        length_Move_Cursor = int(math.hypot(A,B))

        #Need to do some check here. To see that the length only goes up on every move?
        if prev_Hypotenuse_Length <= length_Move_Cursor:
            prev_Hypotenuse_Length = length_Move_Cursor
        else:
            direction = 1
            #print("Direction changed")
            break
        
        #If length is higher than the counter amount break from loop
        #Record certain hypotenuse lengths at a time
        if length_Move_Cursor > movement_length:
            #print(length_Move_Cursor)
            break
  
        #writes the values into a notepad
        file = mouse_Movement_Folder + "\\" + str(length) + ".txt"
        with open(file, "a") as f:
            f.write(str(x) + "," + str(y) + "\n") 

    return file, direction

def record_macros():
    #Press button g to start recording the macro
    state_c_key = win32api.GetKeyState(0x43)
    #Length of mouse movements
    counter = 1
    second_counter = 0
    while True:           
        second_counter += 1
        if second_counter % 5 == 0:
            counter += 1
                    
        file, direction = mouse_cap(len(os.listdir(mouse_Movement_Folder)), counter)

        if direction == 1:
            delete_File(file)
        else:
            continue


record_macros()
