import win32api
import time
import os
import win32con
from math import acos, degrees
import math
import random
#from DegreeFitter import adjust_Degree

#Location of recorded mouse movements
mouse_Movement_Folder = "C:\\Users\\Omistaja\\Desktop\\BOTPROJECT\\MoveCursor\\mousemovementfolder\\"


#Pythagorean theorem and you can change to any degree while keeping the same mouse movement length
#a^2 + b^2 = c^2
def adjust_Degree(end_Degree, mouse_File_Name):
    #Get data from the file name
    mouse_File_Name = mouse_File_Name.split(",")
    #print(mouse_File_Name)
    #Degree of hypotenuse
    hypotenuse_degree = mouse_File_Name[0]
    #Total x length
    x_Length = mouse_File_Name[1]
    #Total y length
    y_Length = mouse_File_Name[2]
    
    #C value must stay the same -> same as length
    c = int(x_Length)*int(x_Length) + int(y_Length)*int(y_Length)
    c = math.sqrt(c)

    #Change to radians
    radian = (end_Degree/360)*(2*(math.pi))

    #sec trigometry
    sec = 1/math.cos(radian)

    #x and y new lengths
    delta_x2 = c/sec
    delta_y2 = c*math.sqrt(1-1/(sec**2))

    #To reach these lengths
    #x needs to change by
    x_Total_Change = float(x_Length) - delta_x2

    #y needs to change by
    y_Total_Change = float(y_Length) - delta_y2
    
    return x_Total_Change, y_Total_Change


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
        ##X modifiers
        if x_Change_Modifier == 1:
            new_x = x + ((start_x - x)*2)
        if x_Change_Modifier == 0:
            new_x = x
        if x_Change_Modifier == -1:
            new_x = x + ((start_x - x)*2)

        #Y modifiers
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

def Change_Coordinates(length, degree_To_Change_To, zone_To, x_original, y_original):
    #Picking random mouse movement file according to the length
    mouse_File_Name = pick_Random_File(mouse_Movement_Folder, length)
    
    #Get the lengths of mouse movements in a text file
    length_Of_File = get_Folder_Length(mouse_Movement_Folder, length, mouse_File_Name)

    #Original mouse movement file degree
    mouse_File_Degree = mouse_File_Name.split(",")[0]

    #Original mouse movement zone
    mouse_File_Zone = mouse_File_Name.split(",")[3].strip(".txt")

    #Gets the total amount x and y needs to be changed to reach a certain degree
    x_Total_Change, y_Total_Change = adjust_Degree(degree_To_Change_To, mouse_File_Name)

    #Get the change x and y needs to change per coordinate in file
    x_Change_Per_Coordinate = x_Total_Change/float(length_Of_File)
    y_Change_Per_Coordinate = y_Total_Change/float(length_Of_File)

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
                #Split values from text file
                x, y = line.split(",")
                
                #Getting starter x and y values that can be modified later
                if counter == 0:
                    start_x = x
                    start_y = y
                    
                    #Get the difference between current mouse position and text file
                    x_now, y_now = win32api.GetCursorPos()
                    x_modifier = int(x_now) - int(x)
                    y_modifier = int(y_now) - int(y)

                    #Y value changes differently than x value on screen, opposite from calculation
                    if y_modifier > 0:
                        y_modifier = abs(y_modifier)
                        
                counter += 1
                #print(length_Of_File)
                sleep_time = 10000**36500

                #Could be more accurate, maybe function for this?  
                x_Change_Amount = round(x_Change_Per_Coordinate*counter)
                y_Change_Amount = round(-(y_Change_Per_Coordinate*counter))

                #Changes zone
                x_Mouse, y_Mouse = Mouse_Coordinate_Change(int(mouse_File_Zone), zone_To, int(start_x), int(start_y), int(x), int(y))

                #Fitts law number
                fitts_Number = random.randint(16,34)

                #Mouse movement according to new x and y coordinates
                if zone_To == 1:
                    x_Position = x_Mouse + int(x_modifier) - int(x_Change_Amount)
                    y_Position = y_Mouse + int(y_modifier) - int(y_Change_Amount)
                    win32api.SetCursorPos((x_Position , y_Position))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
                    if counter > length_Of_File-fitts_Number:       
                        sleep_time = 10000**36500
                    
                if zone_To == 2:
                    x_Position = x_Mouse + int(x_modifier) + int(x_Change_Amount)
                    y_Position = y_Mouse + int(y_modifier) - int(y_Change_Amount)
                    win32api.SetCursorPos((x_Position , y_Position))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
                    #Random Fitt's Law fix later
                    if counter > length_Of_File-fitts_Number:       
                        sleep_time = 10000**36500
                    
                if zone_To == 3:
                   x_Position = x_Mouse + int(x_modifier) + int(x_Change_Amount)
                   y_Position = y_Mouse + int(y_modifier) + int(y_Change_Amount)
                   win32api.SetCursorPos((x_Position , y_Position))
                   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
                   if counter > length_Of_File-fitts_Number:       
                        sleep_time = 10000**36500
                   
                if zone_To == 4:
                   x_Position = x_Mouse + int(x_modifier) - int(x_Change_Amount)
                   y_Position = y_Mouse + int(y_modifier) + int(y_Change_Amount)
                   win32api.SetCursorPos((x_Position , y_Position))
                   win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
                   if counter > length_Of_File-fitts_Number:       
                        sleep_time = 10000**36500

    #What if only one has changed? Add this later. For example only x values changes and y stays the same or other way around.

    #If x or y hasn't changed play the original mouse movement text file, need to check for zone tho?
    if x_Total_Change == 0 and y_Total_Change == 0:
        counter = 0
        with open(mouse_Movement_Folder + str(length) + "\\" + mouse_File_Name, "r") as f:
            for line in f:
                line = line.strip("\n")
                x, y = line.split(",")
                #Getting starter x and y values that can be modified later
                if counter == 0:
                    start_x = x
                    start_y = y
                    #Set counter to 1
                    counter = 1
                sleep_time = 10000**36500
                x_Mouse, y_Mouse = Mouse_Coordinate_Change(int(mouse_File_Zone), zone_To, int(start_x), int(start_y), int(x), int(y))

                #Mouse movement according to new x and y coordinates
                if zone_To == 1 or zone_To == 2 or zone_To == 3 or zone_To == 4:
                    win32api.SetCursorPos((x_Mouse, y_Mouse))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)

def move_Cursor(x_To, y_To):
    #Get original mouse position
    x, y = win32api.GetCursorPos()

    #Zone type
    if x < x_To and y > y_To:
        zone_Move_Cursor = 1
    if x > x_To and y > y_To:
        zone_Move_Cursor = 2
    if x > x_To and y < y_To:
        zone_Move_Cursor = 3
    if x < x_To and y < y_To:
        zone_Move_Cursor = 4
        
    #Values to get degree, length of mouse movement to certain x and y position
    A = abs(x-x_To)
    B = abs(y-y_To)
    
    #calculate hypotenuse length
    length_Move_Cursor = int(math.hypot(A,B))
    #print(length_Move_Cursor)
    
    #calc degree of angle
    angle = math.atan2(A,B)
    degree_Move_Cursor = (90-(angle*180)/math.pi)
    degree_Move_Cursor = (round(degree_Move_Cursor, 4))
    
    #in case higher than 89 or lower than 1 needs some fixes in code
    #To make sure degree is not 0 or 90
    if degree_Move_Cursor > 89:
        degree_Move_Cursor -= 1
    if degree_Move_Cursor < 1:
        degree_Move_Cursor += 1

    #Function that plays mouse movement from text file and adjusts degree properly
    Change_Coordinates(length_Move_Cursor, degree_Move_Cursor, zone_Move_Cursor, x, y) 
    
#move_Cursor(555,480)



            





