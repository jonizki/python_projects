import math
import time
import random
from math import acos, degrees
import os

#Pythagorean theorem and you can change to any degree while keeping the same mouse movement length
#a^2 + b^2 = c^2
def adjust_Degree(end_Degree, mouse_File_Name):
    #Get data from the file name
    mouse_File_Name = mouse_File_Name.split(",")
    #print(mouse_File_Name)
    #Degree of hypotenuse
    hypotenuse_degree = mouse_File_Name[0]
    #Total x grow amount
    x_Grow = mouse_File_Name[1]
    #Total y grow amount
    y_Grow = mouse_File_Name[2]
  
    #C value must stay the same -> same as length
    hypotenuse_To_Squared = int(x_Grow)*int(x_Grow) + int(y_Grow)*int(y_Grow)

    #Degree needs to grow
    if float(end_Degree) > float(hypotenuse_degree):
        #Loop until right degree value is found
        for i in range(10000):
            x_value = int(x_Grow) - 0.1 * i
            x_squared = (x_value)*(x_value)
            y_value = hypotenuse_To_Squared - x_squared
            y_value = math.sqrt(y_value)
            length = float(math.hypot(x_value,y_value))
            #print(length)

            angle = math.atan2(float(x_value),float(y_value))
            degree = 90-(angle*180)/math.pi
            degree = (round(degree, 4))

            #Close as possible to the target degree, 0.1 change is plausible
            #We check if the current degree fits between these two values
            target_Degree_Negative = end_Degree - 0.1
            target_Degree_Positive = end_Degree + 0.1
            
            if degree > target_Degree_Negative and degree < target_Degree_Positive:   
                #print(degree)
                x_Total_Change = float(x_Grow) - x_value
                y_Total_Change = float(y_Grow) - y_value
                break

    #Degree need to go lower            
    if float(end_Degree) < float(hypotenuse_degree):
        #Loop until right degree value is found
        for i in range(10000):
            x_value = int(x_Grow) + 0.1 * i
            x_squared = (x_value)*(x_value)
            y_value = hypotenuse_To_Squared - x_squared
            y_value = math.sqrt(abs(y_value))
            length = float(math.hypot(x_value,y_value))
            #print(length)

            angle = math.atan2(float(x_value),float(y_value))
            degree = 90-(angle*180)/math.pi
            degree = (round(degree, 4))

            #Close as possible to the target degree, 0.1 change is plausible
            #We check if the current degree fits between these two values
            target_Degree_Negative = end_Degree - 0.1
            target_Degree_Positive = end_Degree + 0.1
            
            if degree > target_Degree_Negative and degree < target_Degree_Positive:   
                print(degree)
                x_Total_Change = float(x_Grow) - x_value
                y_Total_Change = float(y_Grow) - y_value
                break

    #If the values are same degree has not changed.
    if float(end_Degree) == float(hypotenuse_degree):
        x_Total_Change = 0
        y_Total_Change = 0

    print(x_Total_Change)
    print(y_Total_Change)
    
    return x_Total_Change, y_Total_Change

#x, y = adjust_Degree(x_Grow, y_Grow, 30, hypotenuse_degree)
#print(x,y)







