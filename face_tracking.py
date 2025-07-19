import cv2, time
import numpy as np
from drone_init import drone

cap = cv2.VideoCapture(1)

drone.takeoff()
drone.send_rc_control(0, 0, 25, 0)
time.sleep(2.5)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

w, h = 360, 240
fbr = [6200, 6800]
pid = [0.4, 0.4, 0]
pe = 0

def trace(obj, info):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pe)
    speed = int(np.clip(speed, -100, 100))

    if area > fbr[0] and area < fbr[1]:
        fb = 0
    elif area > fbr[1]:
        fb = -20
    elif area < fbr[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    obj.send_rc_control(0, fb, 0, speed)
    return error

def track(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, 1.1, 8
    )

    center = []
    area = []

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = x + w // 2
        cy = y + h // 2

        area = w * h
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

        center.append([cx, cy])
        area.append(area)

    if len(center) > 0:
        id = area.index(max(area))
        return frame, [center[id], area[id]]
    else:
        return frame, [[0, 0], 0]

def capture():
    frame = drone.get_frame_read().frame
    frame = cv2.resize(frame, (w, h))
    frame, info = track(frame)
    pe = trace(drone, info)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        return False
    else:
        return True

while(True):
    if capture() == False:
        break



