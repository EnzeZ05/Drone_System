import numpy as np
import math
import cv2

speed_x = 11.4514
ang_v = 36
itv = 0.25

ditv = speed_x * itv
aitv = ang_v * itv

x = y = 500
d = a = 0
yaw = 0

def reset():
    global d
    d = 0

def upd_dist(coeff):
    global d
    d = coeff * ditv

def upd_angle(x):
    global a
    a = x

def upd_rotate(coeff):
    global yaw
    yaw += coeff * aitv

def get_cartesian():
    global x, y
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

def graphing():
    global x, y
    img = np.zeros((1000, 1000, 3), np.uint8)
    cv2.circle(img, (x, y), 5, (0, 0, 255), cv2.FILLED)
    cv2.imshow('image', img)
    cv2.waitKey(1)
