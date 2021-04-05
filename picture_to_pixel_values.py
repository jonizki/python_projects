from PIL import Image

#image you want to turn to pixels
image_name = "new"

#Image to extract data from
im = Image.open(image_name + ".png")

#Extracting pixel values
pix_val = list(im.getdata())

#Gets the pixel values and appends them to a text file
with open(image_name + ".txt", "a") as f:
    for x in pix_val:
        f.write(str(x).strip("()") + "\n")
    
    


