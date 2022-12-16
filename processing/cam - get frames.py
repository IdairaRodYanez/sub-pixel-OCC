# script that fetches all the frames that make up a video

import cv2 as cv
import time

cap= cv.VideoCapture('medium/video.mjpeg')

# Used as counter variable
count = 0
  
# Checks if the extraction of the frame was correct
success, image = cap.read()
  
while success:

    # Saves the frames with frame-count
    cv.imwrite("medium/frame%d.jpg" % count, image)
    
    # function extract frames
    success, image = cap.read()
  
    count += 1

print("The total number of frames in this video is ", count)

