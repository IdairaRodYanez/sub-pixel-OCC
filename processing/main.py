from multiprocessing import Pool, TimeoutError
import multiprocessing as mp
from socket import timeout
import time
import simplifier
import correlator
import numpy as np
from functools import partial
from skimage import measure
import matplotlib.pyplot as plt
import cv2
import loader
import random

# Variables
# multiprocessing
frames_queue = mp.Queue()
amount_of_subregion = mp.cpu_count()

# frame estructure
tiempo_bit = 4/30
num_bits_trama = 15
fps = 30
num_tramas = 2 # fijo

# image processing
index_unified = []
images_simplifier = []
images_correlator = []

# CONFIGURAR
light_umbral = 240
init_frame = 0

# metodo que elimina los pixeles vecinos (asi como su trama asociada), dejando unicamente el primero que aparezca en la lista definitiva de pixeles
def delete_neighbouring_pixels(array, tramas, pixel_limit):  
    position_to_delete = []
    # obtenemos los indices de los pixeles vecinos
    for i in range(0, len(array)-1):
        for j in range(i+1, len(array)):
            x = array[i][0] - array[j][0]
            y = array[i][1] - array[j][1]

            if np.abs(x+y) < pixel_limit:
                position_to_delete.append(j)
    
    # eliminamos las posiciones de los pixeles vecinos
    position_to_delete = [*set(position_to_delete)] # eliminamos posiciones repetidas
    position_to_delete.sort(reverse = True) # ordenamos en orden decreciente
    for i in position_to_delete:
        array.pop((i))
        tramas.pop((i))
    return array, tramas

if __name__ == '__main__':
  number_of_frames = int(tiempo_bit*num_bits_trama*num_tramas*fps) # 1 trama - 2 second - 60 frames of the camera - camera: 30 frames/second
  print('The number of frames are: '+str(number_of_frames))
  pool = mp.Pool(processes = amount_of_subregion)    

  # CAMARA
  capture_process = mp.Process(target=loader.get_frames, args=(number_of_frames, frames_queue, init_frame)) # inicias proceso de captura
  capture_process.start()
        
  count = 0
  second_count = 0
  # SIMPLIFIER
  while count < number_of_frames: 
    timref = time.time()
    image = frames_queue.get(timeout=20) # espera por elemento de la camara
    if (count == 1):
      if (np.mean(image) < 30):          # get threshold based on the average brightness of the image
        light_umbral = 120
      elif (np.mean(image) < 80):
        light_umbral = 240
      else: 
        light_umbral = 250

    if (count < 60):                      # almacena solo la mitad de los frames porque con ellos es mas que suficiente para detectar un "1" en transmision 
      images_simplifier.append(image)
    images_correlator.append(image)
    if (len(images_simplifier)%amount_of_subregion==0) & (count<60) & (len(images_simplifier)>0):
      index_per_image = pool.map(partial(simplifier.get_possible_tx, light_umbral), iterable = images_simplifier) # obtiene los pixeles potencialmente tx de la imagen capturada
      images_simplifier = []                                                                           # se resetea almacen de imagenes para el simplificador
      second_count = second_count + 1
      # anexamos arrays de pixeles
      if second_count == 1:
        index_unified = index_per_image.copy()                                              # no se pueden concatenar arrays a uno vacio, asi que en el primer caso se copia                                        
      else:
        for c in range (0, amount_of_subregion):
          index_unified[c] = np.concatenate((index_unified[c], index_per_image[c]))         # concatenamos todos los pixeles considerados potenciales txs
    # incrementamos cuenta
    count = count + 1  
          
  index_possible_tx = index_unified.copy()
  for c in range (0, len(index_unified)):
    index_possible_tx[c] = np.unique(index_unified[c], axis= 0) # eliminamos los elementos repetidos
    
  # TRANSFORM ARRAY DE CPU RESULTADOS CON FLATTEN - format [[[a,b] ...],[[c,d] ...]] (subsections due to multiprocessing) to [[a,b], [c,d] ...]       
  array = [index_possible_tx[0][1]]
  for c in range(0,len(index_possible_tx)): # accedemos a cada uno de los resultados del multiprocessing
    for d in range(1, len(index_possible_tx[c])): # escogemos todos los elementos de cada resultado del multiprocessing, menos el primer elemento [0,0]    
      array.append(index_possible_tx[c][d])

  index_possible_tx = np.unique(array, axis = 0) # eliminamos los elementos repetidos
  timout = time.time()
  print('Tiempo de simplificación:')
  print(timout-timref)
  print('Hay '+ str(np.shape(index_possible_tx)[0]) + ' candidatos')
  
  
  # CORRELATOR
  tima = time.time()
  [pixels, tramas] = correlator.get_tx_pixels(images_correlator, index_possible_tx, light_umbral) # get pixels with a std in a specific range
  
  # ELIMINAMOS PIXELES VECINOS
  [pixels, tramas] = delete_neighbouring_pixels(pixels, tramas, 8)
  
  print('Hay ' + str(np.shape(pixels)[0]) + ' transmisores')
  print(pixels)
  timb = time.time() 
  print('Tiempo de correlación:') 
  print(timb-tima)   
  
  ########## OBSERVACION DE RESULTADOS ###########
  # GRABAMOS IMAGEN PARA PODER USARLA CON CHECKPXL
  cv2.imwrite('imagen.jpg', images_correlator[0])
  
  # REPRESENTAMOS PIXELES
  gray = images_correlator[0] # tomamos imagen 
  id = 0
  for p in pixels:
    [y,x] = p
    id += 1
    cv2.putText(gray, "#{}".format(id), (x, y - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2, cv2.LINE_AA) 
  cv2.imshow("Possible TXs labeled", gray)
  cv2.waitKey(0)
 
  # REPRESENTAMOS TRAMA
  id = 1
  for y in tramas:
    print(y)
    plt.rcParams["figure.autolayout"] = True
    x = list(range(0,number_of_frames))

    plt.title("Frame graph {}".format(id))
    plt.ylabel('Luminosity in gray scale')
    plt.xlabel('Frames')
    plt.plot(x, y, color="red")
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # REPRESENTAMOS HISTOGRAMA
    plt.rcParams["figure.autolayout"] = True
    (counts, bins, patches) = plt.hist(y)
    plt.title("Frame graph {}".format(id))
    plt.xlabel("Luminosidad")
    plt.ylabel("Densidad")
    plt.show()

    id += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()

