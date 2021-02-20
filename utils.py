#!/usr/bin/env python3
import cv2
import numpy as np
import socket
import ssl
import pickle
import struct
import os
from config import SERVER_SERT, SERVER_KEY

def load_image(path):
    image = cv2.imread(path)
    image=cv2.resize(image, (700,700)) # resize the frame if you want       
    return image

def send_image(image, HOST,PORT,allow_ssl: bool, name, IMG_DTYPE):
    if allow_ssl:
        sendsocket = ssl.wrap_socket(socket.socket(socket.AF_INET,socket.SOCK_STREAM)) # IPv4, TCP
    else:
        sendsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # IPv4, TCP
    
    sendsocket.connect((HOST,PORT))
    image=image.astype('uint16')
    print(name,'Image format:',image.dtype)
    print (name,': media sending')
    data = pickle.dumps(image)
    # Send message length first
    message_size = struct.pack(IMG_DTYPE, len(data)) ### CHANGED
    # Then data
    sendsocket.sendall(message_size + data)
    sendsocket.close()
    return image

def image_receive(HOST,PORT,allow_ssl: bool, name, IMG_DTYPE):
    if allow_ssl:
        receivesocket = ssl.wrap_socket(socket.socket(socket.AF_INET,socket.SOCK_STREAM),certfile=SERVER_SERT, keyfile=SERVER_KEY  ) # IPv4, TCP
    else:
        receivesocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # IPv4, TCP
    
    print (name,' Socket created')
    receivesocket.bind((HOST,PORT))
    print (name,' Socket bind complete')
    receivesocket.listen(10)
    print (name,' Socket now listening')
    conn,addr=receivesocket.accept()
    print (name,' Connection accepted')
    data = b'' # byte literal instead of a string literal
    payload_size = struct.calcsize(IMG_DTYPE) # Change "H" to "L" if you have a larger frame.
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(IMG_DTYPE, packed_msg_size)[0]
    #msg_size = int(msg_size) # indexes must be integers
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    receivesocket.close()
    return frame