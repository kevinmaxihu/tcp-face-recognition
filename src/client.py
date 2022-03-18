import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np
import imutils

def main(args = None):
 
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(('0.tcp.ngrok.io', 19194))
    client_socket.connect(('10.10.69.59', 8485))

    cam = cv2.VideoCapture(0)
    img_counter = 0

    #encode to jpeg format
    #encode param image quality 0 to 100. default:95
    #if you want to shrink data size, choose low image quality.
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

    while True:
        ret, frame = cam.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # 影像縮放
        frame = imutils.resize(frame, width=320)
        # 鏡像
        frame = cv2.flip(frame,180)
        result, image = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(image, 0)
        size = len(data)

        if img_counter%2==0:
            client_socket.sendall(struct.pack(">L", size) + data)
            cv2.imshow('client',frame)
            
        img_counter += 1

        # 若按下 q 鍵則離開迴圈
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    cam.release()

if __name__ == '__main__':
    main()