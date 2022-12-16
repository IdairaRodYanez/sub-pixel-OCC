# script that adds to the program queue the frames associated to a range of images on a database

import cv2 as cv
import numpy as np
import multiprocessing as mp

# Method that return x frames in gray scale from a database of jpg images
#   Parameters: 
#   number_of_frames - number of frames that are studied from .npy file
#   init_frame - initial frame from which processing is applied
#   frames_queue - multiprocessing queue at which frames are appended

def get_frames(number_of_frames, frames_queue, init_frame):
    
    images = []
    try:
        for count in range(init_frame, int(init_frame + number_of_frames)): # 1 trama - 2 second - 60 frames of the camera (camera: 30 frames/second)
          image = cv.imread("medium/frame%d.jpg" % count)
          gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)                      # frame to gray scale
          images.append(gray)                                               # store frame
          frames_queue.put(gray)                                            # add frame to queue
    except:
        print('frame inicial demasiado elevado')

    return images # array of (frameWidth, frameHeight) arrays