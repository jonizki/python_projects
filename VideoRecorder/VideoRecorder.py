import numpy as np
import cv2
import d3dshot



#Initialize d3dshot
d = d3dshot.create(capture_output="numpy")

frames = []

while True:
    screenshot = d.screenshot()
    screenshot = screenshot[...,::-1]
    frames.append(screenshot)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

# Get image height and width
height, width, x_ = frames[0].shape

# initialize video writer
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 60
video_filename = 'output.mp4'
out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

# new frame after each addition of water
for frame in frames:
    #add this array to the video
    out.write(frame)

# close out the video writer
out.release()