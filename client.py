#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import os
#from src.utils import image_to_bytes
from config import HOST, PORT1, IMG_DTYPE
from utils import load_image, send_image
machine_name='CLIENT'
path='test.jpg'
# show what we sended
image=load_image(path)
image=send_image(image,HOST, PORT1,True, machine_name, IMG_DTYPE)
image=image.astype('uint8')

while(1):
    cv2.imshow(machine_name,image)
    k = cv2.waitKey(50)
    if k==27:    # Esc key to stop
        
        break