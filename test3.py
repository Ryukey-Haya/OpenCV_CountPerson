import cv2
import requests,json
import threading,time

def save_picture():
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
    cap.set(cv2.CAP_PROP_FPS, 60)

    if not cap.isOpened():
        return

    ret,frame=cap.read()
    cv2.imwrite('photo.png',frame)

save_picture()
cv2.imshow(cap.read())
cv2.waitKey(0)
