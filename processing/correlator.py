import numpy as np

# serie = set of consecutive equal numbers
# max amount of ones by serie: 9
# max amount of zeros by serie: 10
# min amount of ones by serie: 1
# min amount of zeros by serie: 1
# max amount of rises in two frames: 10
# min amount of rises in two frames: 2
# min amount of ones'series in two frames: 2
# min amount of zeros'series in two frames: 4
# max amount of ones'series in two frames: 10
# max amount of zeros'series in two frames: 10
# amount of frame per bit: 4
# min amount of periods in two frames: 3

# Method that get the position in the frame of possible tx based on the relation of its values over time and the frame format 
def get_tx_pixels(images, posible_tx, light_umbral):
    pixels = []
    tramas = []
    threshold =  0.60*light_umbral

    for posible_tx_count in range(0, len(posible_tx)): # go through array of potentially valid pixels 
        trama = [] 
        trama_10 = []  
        for images_count in range(0, len(images)):         # go through the array of greyscale images
            trama.append(images[images_count][posible_tx[posible_tx_count][0], posible_tx[posible_tx_count][1]]) # create a frame with all the images
        # RISING EDGE
        trama_10 = [0 if x<threshold else 1 for x in trama] # apply threshold to the story
        for r in range(0, len(trama_10)-1):
          trama_10[r] = trama_10[r] - trama_10[r+1]         # get the falling (1) and rising (-1) edges              
            
        rises = trama_10.count(-1)              # rising edges
        if (2 <= rises <= 10):                  # check amount of rises
            # SECOND PERIOD
            ind_down = np.argmax(trama_10)      # get index of first falling edge
            ind_rise = np.argmin(trama_10)      # get index of first rising edge
            period2 = np.abs(ind_down-ind_rise) # get second period
            max = 40
            min = 4
            if ((min - 1  <= period2 <= max + 1) ): #  check that the number of ones and zeros is in a range of minima and maxima and that the period is proportional to 4             
                pixels.append(posible_tx[posible_tx_count])
                tramas.append(trama)
                
    return [pixels, tramas]
