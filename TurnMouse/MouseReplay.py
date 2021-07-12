import win32api
import time
import os
import win32con
from math import acos, degrees
import math
import random
from DegreeFitter import adjust_Degree

#Time.sleep can at minimium sleep 10ms and its a slow function
#Make calculations that respond to the milliseconds needed for mouse movements
#Depends on processor?

#Location of recorded mouse movements
mouse_Movement_Folder = "C:\\Users\\Omistaja\\Desktop\\MouseRepeater-main\\TurnMouse\\mousemovementfolder\\"

#Function to change mouse coordinates
def Mouse_Coordinate_Change(original_zone,new_zone, start_x, start_y, x, y):
    #Possible transformations for mouse movement
    #2,3,4
    #1,3,4
    #1,2,4
    #1,2,3
    #Changes for coordinates
    mousecoords = {
      1: {2:[-1,0], 3:[-1,-1], 4:[0,-1]},
      2: {1:[1,0], 3:[0,-1], 4:[-1,-1]},
      3: {1:[-1,-1], 2:[0,1], 4:[1,0]},
      4: {1:[0,1], 2:[1,1], 3:[-1,0]},
    }
    #Mouse movement zone hasn't changed normal x and y values
    if original_zone == new_zone:
        new_x = x
        new_y = y
    #Mouse movement zone has changed -> change x and y values
    if original_zone != new_zone:
        #Getting modifier values
        x_Change_Modifier, y_Change_Modifier = mousecoords[original_zone][new_zone][0], mousecoords[original_zone][new_zone][1]
        if x_Change_Modifier == 1:
            new_x = x + ((start_x - x)*2)
        if x_Change_Modifier == 0:
            new_x = x
        if x_Change_Modifier == -1:
            new_x = x + ((start_x - x)*2)

        if y_Change_Modifier == 1:
            new_y = y + ((start_y-y)*2)
        if y_Change_Modifier == 0:
            new_y = y
        if y_Change_Modifier == -1:
            new_y = y + ((start_y-y)*2)
        
    return new_x, new_y

#Pick random file from a folder that corresponds to the mouse movement length
def pick_Random_File(mouse_Movement_Folder, length):
    #List all the files in the folder
    files = os.listdir(mouse_Movement_Folder + str(length))
    #Check how many files are in the folder
    amount_Of_Files = len(files)
    #Choose a random file in the folder
    random_Choice = random.randint(0, amount_Of_Files-1)
    #Chosen file
    chosen_Mouse_Movement = files[random_Choice]

    return chosen_Mouse_Movement

#Gets folder length of a given file
def get_Folder_Length(mouse_Movement_Folder, length, mouse_File_Name):
    file_Path = mouse_Movement_Folder + str(length) + "\\" + mouse_File_Name
    with open(file_Path,"r") as f:
        length_Of_File = len(f.readlines())

    return length_Of_File

def Change_Coordinates(length, degree_To_Change_To, zone_To):
    #Picking random mouse movement file according to the length
    mouse_File_Name = pick_Random_File(mouse_Movement_Folder, length)
    #Get the lengths of mouse movements in a file
    length_Of_File = get_Folder_Length(mouse_Movement_Folder, length, mouse_File_Name)

    #Original mouse movement file degree
    mouse_File_Degree = mouse_File_Name.split(",")[0]

    #Original mouse movement zone
    mouse_File_Zone = mouse_File_Name.split(",")[3].strip(".txt")

    #Gets the total amount x and y needs to be changed to reach a certain degree
    x_Total_Change, y_Total_Change = adjust_Degree(degree_To_Change_To, mouse_File_Name)

    print(x_Total_Change)

    x_Change_Per_Coordinate = int(x_Total_Change)/length_Of_File
    y_Change_Per_Coordinate = int(y_Total_Change)/length_Of_File

    #When to start changing x and y coordinates so they reach the required degree
    #Check if degree has changed
    if x_Total_Change != 0 and y_Total_Change != 0:
        #Tracking modifiers
        counter = 0

        x_Change_Amount = 0
        y_Change_Amount = 0
        
        with open(mouse_Movement_Folder + str(length) + "\\" + mouse_File_Name, "r") as f:
            for line in f:
                line = line.strip("\n")
                x, y, ms = line.split(",")
                
                #Getting starter x and y values that can be modified later
                if counter == 0:
                    start_x = x
                    start_y = y
                    
                counter += 1  

                x_Change_Amount = round(x_Change_Per_Coordinate*counter)
                y_Change_Amount = round(y_Change_Per_Coordinate*counter)

                #If the change of degree is higher
                if float(mouse_File_Degree) < degree_To_Change_To:
                    x_Change_Amount = (x_Change_Amount)
                    y_Change_Amount = -(y_Change_Amount)

                #If the change of degree is lower
                if float(mouse_File_Degree) > degree_To_Change_To:
                    x_Change_Amount = (x_Change_Amount)
                    y_Change_Amount = -(y_Change_Amount)

                #Changed x and y mouse coordinates
                x_Mouse, y_Mouse = Mouse_Coordinate_Change(int(mouse_File_Zone), zone_To, int(start_x), int(start_y), int(x), int(y))

                #Mouse movement according to new x and y coordinates
                if zone_To == 1:
                    win32api.SetCursorPos((x_Mouse - x_Change_Amount, y_Mouse - y_Change_Amount))
                    time.sleep(float(ms))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
                if zone_To == 2:
                    win32api.SetCursorPos((x_Mouse + x_Change_Amount, y_Mouse - y_Change_Amount))
                    time.sleep(float(ms))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
                if zone_To == 3:
                   win32api.SetCursorPos((x_Mouse + x_Change_Amount, y_Mouse + y_Change_Amount))
                   time.sleep(float(ms))
                   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
                if zone_To == 4:
                   win32api.SetCursorPos((x_Mouse - x_Change_Amount, y_Mouse + y_Change_Amount))
                   time.sleep(float(ms))
                   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)

    #If both are zero degree has not changed and x or y hasn't changed
    if x_Total_Change == 0 and y_Total_Change == 0:
        counter = 0
        with open(mouse_Movement_Folder + str(length) + "\\" + mouse_File_Name, "r") as f:
            for line in f:
                line = line.strip("\n")
                x, y, ms = line.split(",")
                #Getting starter x and y values that can be modified later
                if counter == 0:
                    start_x = x
                    start_y = y
                    #Set counter to 1
                    counter = 1
                x_Mouse, y_Mouse = Mouse_Coordinate_Change(int(mouse_File_Zone), zone_To, int(start_x), int(start_y), int(x), int(y))

                #Mouse movement according to new x and y coordinates
                if zone_To == 1 or zone_To == 2 or zone_To == 3 or zone_To == 4:
                    win32api.SetCursorPos((x_Mouse, y_Mouse))
                    time.sleep(float(ms))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)

def move_Cursor(x_To, y_To):
    #Get original mouse position
    #x, y = win32api.GetCursorPos()
    x,y = 863,587
    time.sleep(0.2)
    win32api.SetCursorPos((x,y))
    time.sleep(0.2)
    #what zone we going to
    if x < x_To and y > y_To:
        zone_Move_Cursor = 1
        #print("Zone is in the first field")
    if x > x_To and y > y_To:
        zone_Move_Cursor = 2
        #print("Zone is in the second field")
    if x > x_To and y < y_To:
        zone_Move_Cursor = 3
        #print("Zone is in the third field")
    if x < x_To and y < y_To:
        zone_Move_Cursor = 4
        #print("Zone is in the fourth field")
        
    #Values to get degree, length of mouse movement to certain x and y position
    A = abs(x-x_To)
    B = abs(y-y_To)
    
    #calculate hypotenuse length
    length_Move_Cursor = int(math.hypot(A,B))
    print("length: " + str(length_Move_Cursor))
    
    #calc degree of angle
    angle = math.atan2(A,B)
    degree_Move_Cursor = (90-(angle*180)/math.pi)-10
    degree_Move_Cursor = (round(degree_Move_Cursor, 4))
    
    #in case higher than 89 or lower than 1 needs some fixes in code
    if degree_Move_Cursor > 89:
        degree_Move_Cursor -= 1
    if degree_Move_Cursor < 1:
        degree_Move_Cursor += 1
    print("degree: " + str(degree_Move_Cursor))

    #Function that plays mouse movement from text file and adjusts degree properly
    Change_Coordinates(length_Move_Cursor, degree_Move_Cursor, zone_Move_Cursor)
    
move_Cursor(992,497)



            





