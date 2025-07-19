from drone_init import drone
import time
import cv2
global img

def capture():
    global img
    img = drone.get_frame_read().frame
    cv2.waitKey(1)
    return img

def display():
    global img
    img = capture()
    img = cv2.resize(img, (640, 480))
    cv2.imshow('frame', img)

def save():
    cv2.imwrite(f'Drone/images/{time.time()}.jpg', capture());