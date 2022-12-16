# script that records for x seconds a video in y format with the camera connected to the raspberry pi

import picamera
import time

num_of_seconds = 560

frameHeight = 1088
frameWidth = 1920

with picamera.PiCamera() as camera:
    camera.resolution = (frameWidth, frameHeight)
    camera.framerate = 30
    camera.shutter_speed = 32900
    camera.drc_strength = 'off' # the dynamic range compression that the camera applies to the images is disabled

    time.sleep(2)  # camera needs time to stablish exposure speed

    camera.start_recording('highExposure/mjpeg.mjpeg')
    camera.wait_recording(num_of_seconds)
    camera.stop_recording()
