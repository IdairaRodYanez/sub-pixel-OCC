import cv2 as cv
import numpy as np
import multiprocessing as mp

# Method that return x frames in gray scale from the PC camera
#   Parameters: 
#   number_of_frames - number of frames that the camera takes
#   frames_queue - multiprocessing queue at which frames are appended
def get_frames(number_of_frames, frames_queue):
    cam = cv.VideoCapture(0)
    cam.set(cv.CAP_PROP_FPS, 30)

    images = []

    for count in range(0, (number_of_frames)): # 1 trama - 2 second - 60 frames of the camera - camera: 30 frames/second
        success, image = cam.read()                                     # take frame
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)                    # frame to gray scale
        images.append(gray)                                             # store frame
        frames_queue.put(gray)

    return images # array formado por matrices 660, 440