from PIL import Image
import numpy as np

#text file where pixel values are located
text_File = "new.txt"

#list of all the pixels
pixels = []

#Loops through the list and appends tuples to pixels list
with open(text_File, "r") as f:
    pixel_Values = []
    for line in f:
        line = line.strip("\n")
        line = tuple(map(int, line.split(', ')))
        pixel_Values.append(line)
    pixels.append(pixel_Values)

#creates array from pixels
array = np.array(pixels, dtype=np.uint8)
new_image = Image.fromarray(array)
#saves image
new_image.save('new.png')

