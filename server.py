#!/usr/bin/env python3
import socket
import sys
import cv2
import numpy as np
import struct ## new
from utils import image_receive
from config import HOST, PORT2, IMG_DTYPE
machine_name='SERVER'

def remove_noise(image):
    image = cv2.medianBlur(image, 3)
    return image

image = image_receive(HOST, PORT2,True, machine_name, IMG_DTYPE)
image=image.astype('uint8')
print (machine_name,': showing')

image = remove_noise(image) # apply denoise filter

while(1):
    cv2.imshow(machine_name,image)
    k = cv2.waitKey(50)
    if k==27:    # Esc key to stop
        cv2.imwrite("denoised_image.jpg",image)
        break