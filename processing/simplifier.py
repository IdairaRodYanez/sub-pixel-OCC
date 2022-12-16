from skimage import measure
import numpy as np
import cv2

# Method that get the position in the frame of possible tx based on the luminosity and size of grupe of pixels
# Parameters:
# Light_umbral - Threshold used to determine whether or not it is an LED
# Gray - Frame in gray format in which possible tx are searched
def get_possible_tx(light_umbral, gray):         
    
    index_pixels = []             # array that contains the x,y pairs associated with the possible txs
    index_pixels.append([0,0])    # initial element is added to avoid errors related to  null elements 
    max_region_size = 16          # maximum Region Of Interest (ROI)

    # Threshold the image to REVEAL LIGHT REGIONS in the gray image
    (T, thresh) = cv2.threshold(gray, light_umbral, 255, cv2.THRESH_BINARY_INV & cv2.THRESH_OTSU)

    # Join the light pixels if possible
    labels, num = measure.label(thresh, background=0, return_num=True) # returns the set of labelled pixel regions (pixels connected in some sense) and the number of existing regions 
    # loop over the unique components
    for label in np.unique(labels):
        labelMask = np.zeros(thresh.shape, dtype="uint8") # empty mask
        labelMask[labels == label] = 255                  # where the value of label and labels matches writes 255 (we are adding one "layer" per label)
        numPixels = cv2.countNonZero(labelMask)           # count non-zero number of pixels  
        index_region = np.where(labelMask != 0)           # get indexs of pixels that conform the region in the frame
        # if the number of pixels in the component is sufficiently short, store central pixel
        if numPixels < max_region_size:                   # if number of pixels is less than maximum
            if np.shape(index_region)[1] == 1:            # if the region consists of only one pixel
                index_pixels.append([index_region[0][0],index_region[1][0]]) # append that pixel
            else:                                         # if the region has more than one pixel
                index_pixels.append([index_region[0][round((np.shape(index_region)[1])/2)],index_region[1][round((np.shape(index_region)[1])/2)]]) # append the central pixel
    unique_index_pixels = np.unique(index_pixels, axis=0) # remove the repeated elements
    
    return unique_index_pixels 