import win32api
import time
import os
import win32con
from math import acos, degrees
import math
import random
from DegreeFitter import adjust_Degree

#Location of recorded mouse movements
mouse_Movement_Folder = "C:\\Users\\Omistaja\\Desktop\\TurnMouse\\mousemovementfolder\\"

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
        #Gettings modifier values
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

def Change_Coordinates():
    #Length of the mouse movement -> add this
    length = 212
    #Picking random mouse movement file according to the length
    mouse_File_Name = pick_Random_File(mouse_Movement_Folder, length)
    #Get the lengths of mouse movements in a file
    length_Of_File = get_Folder_Length(mouse_Movement_Folder, length, mouse_File_Name)

    #Original mouse movement file degree
    mouse_File_Degree = mouse_File_Name.split(",")[0]
    #What the degree needs to be, get this from the mouse length function
    degree_To_Change_To = 15
    #Gets the total amount x and y needs to be change to reach a certain degree
    x_Total_Change, y_Total_Change = adjust_Degree(degree_To_Change_To, mouse_File_Name)

    #When to start changing x and y coordinates so they reach the required degree
    x_Counter_Change = int(length_Of_File/x_Total_Change)
    y_Counter_Change = int(length_Of_File/y_Total_Change)

    #Tracking modifiers
    x_Change_Amount = 0
    y_Change_Amount = 0
    counter = 0
    with open(mouse_Movement_Folder + str(length) + "\\" + mouse_File_Name, "r") as f:
        for line in f:
            line = line.strip("\n")
            x, y = line.split(",")
            #Getting starter x and y values that can be modified later
            if counter == 0:
                start_x = x
                start_y = y
            counter += 1

            #If the change of degree is positive
            if float(mouse_File_Degree) > degree_To_Change_To:
                if counter % x_Counter_Change == 0:
                    x_Change_Amount -= 1
                if counter % y_Counter_Change == 0:
                    y_Change_Amount -= 1

            #If the change of degree is negative
            if float(mouse_File_Degree) < degree_To_Change_To:
                if counter % x_Counter_Change == 0:
                    x_Change_Amount += 1
                if counter % y_Counter_Change == 0:
                    y_Change_Amount += 1

            zone_To = 1
            #Changed x and y mouse coordinates    
            x_Mouse, y_Mouse = Mouse_Coordinate_Change(1,zone_To, int(start_x), int(start_y), int(x), int(y))

            #Mouse movement according to new x and y coordinates
            if zone_To == 1:
                win32api.SetCursorPos((x_Mouse - x_Change_Amount, y_Mouse - y_Change_Amount))
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
            if zone_To == 2:
                win32api.SetCursorPos((x_Mouse + x_Change_Amount, y_Mouse - y_Change_Amount))
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
            if zone_To == 3:
               win32api.SetCursorPos((x_Mouse + x_Change_Amount, y_Mouse + y_Change_Amount))
               time.sleep(0.01)
               win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)
            if zone_To == 4:
               win32api.SetCursorPos((x_Mouse - x_Change_Amount, y_Mouse + y_Change_Amount))
               time.sleep(0.01)
               win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_Mouse, y_Mouse,0,0)


Change_Coordinates()





