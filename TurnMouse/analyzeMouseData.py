import math
import time
import random
from math import acos, degrees
import os


mouse_Folder = "C:\\Users\\Omistaja\\Desktop\\TurnMouse\\mousemovements\\"
mouse_Movement_Folder = "C:\\Users\\Omistaja\\Desktop\\TurnMouse\\mousemovementfolder\\"

amount_Of_Files = len(os.listdir(mouse_Folder))
counter = 0
second_counter = 0
for i in range(amount_Of_Files):
    #Original mouse movements
    x_Coords = []
    y_Coords = []
    #Adding mouse movements to arrays
    with open(mouse_Folder + str(i) + ".txt", "r") as file:
        for line in file:
            counter += 1
            if counter == 1:
                line = line.strip("\n")
                x, y = line.split(",")
                x_Coords.append(x)
                y_Coords.append(y)
            if counter > 1:
                line = line.strip("\n")
                x, y = line.split(",")
                if x_Coords[second_counter] == x and y_Coords[second_counter] == y:
                    print("Mouse movement already in file:")
                else:   
                    x_Coords.append(x)
                    y_Coords.append(y)
                    second_counter += 1

    #X axis
    x_First = int(x_Coords[0])
    x_Second = int(x_Coords[-1])   
    A = abs(x_First-x_Second)
    print(A)
    #Y Axis
    y_First = int(y_Coords[0])
    y_Second = int(y_Coords[-1])
    B = abs(y_First-y_Second)
    print(B)

    #Length of movements
    length = int(math.hypot(A,B))
    print(length)

    #Calculating angle of mouse movement
    angle = math.atan2(A,B)
    degree = 90-(angle*180)/math.pi
    degree = (round(degree, 4))
    print(degree)

    #Calculating zones where each triangle is located in
    if x_First < x_Second and y_First > y_Second:
        zone = 1
        print("Zone is in the first field")
    if x_First > x_Second and y_First > y_Second:
        zone = 2
        print("Zone is in the second field")
    if x_First > x_Second and y_First < y_Second:
        zone = 3
        print("Zone is in the third field")
    if x_First < x_Second and y_First < y_Second:
        zone = 4
        print("Zone is in the fourth field")
    
    with open(mouse_Movement_Folder + str(length) + "\\" + str(degree) + "," + str(A) + "," + str(B) + "," + str(zone) + ".txt", "w") as file:
        for i in range(len(x_Coords)):
            file.write(str(x_Coords[i]) + "," + str(y_Coords[i]) + "\n")
            
    #reset counters     
    counter = 0
    second_counter = 0
