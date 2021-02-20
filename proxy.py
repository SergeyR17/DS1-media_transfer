#!/usr/bin/env python3
import socket
import sys
import cv2
import numpy as np
import random
import struct ## new
from utils import image_receive
from config import HOST, PORT1, PORT2, IMG_DTYPE
from utils import load_image, send_image

machine_name='PROXY'
path='test.jpg'

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


image = image_receive(HOST, PORT1,True, machine_name, IMG_DTYPE)
image=image.astype('uint8')

image=sp_noise(image,0.01) # apply noize

image=send_image(image,HOST, PORT2,True, machine_name, IMG_DTYPE)
image=image.astype('uint8')

# show what we sended
print (machine_name,': showing')
while(1):
    cv2.imshow(machine_name,image)
    k = cv2.waitKey(100)
    if k==27:    # Esc key to stop
        cv2.imwrite("noised_image.jpg",image)
        break

