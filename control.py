from image_capture import display
from functools import update_wrapper
from vector import upd_rotate
import drone_init
from drone_init import drone

import keyboard as kb
import vector
import time

in_air = False

def def_mat():
    return [25, 25, 25, 25]

def transformation():
    return [[1, 0, 0, 0], [-1, 0, 0, 0],
            [0, 1, 0, 0], [0, -1, 0, 0],
            [0, 0, 1, 0], [0, 0, -1, 0],
            [0, 0, 0, 1], [0, 0, 0, -1]]

def movement():
    _dir = kb.keyboard()
    mat = transformation()
    vector.reset()

    if in_air:
        if _dir == 'a':
            vector.upd_dist(1)
            vector.upd_angle(-180)
            return mat[0]
        elif _dir == 'd':
            vector.upd_dist(-1)
            vector.upd_angle(180)
            return mat[1]

        if _dir == 'w':
            vector.upd_dist(1)
            vector.upd_angle(270)
            return mat[2]
        elif _dir == 's':
            vector.upd_dist(-1)
            vector.upd_angle(-90)
            return mat[3]

        if _dir == 'z':
            return mat[4]
        elif _dir == 'x':
            return mat[5]

        if _dir == 'q':
            upd_rotate(1)
            return mat[6]
        elif _dir == 'e':
            upd_rotate(-1)
            return mat[7]

        return [0, 0, 0, 0]

def main():
    global in_air
    mat = def_mat()
    drone_init._launch()
    time.sleep(2)
    # drone_init._takeoff()
    in_air = True

    if in_air:
        while True:
            offset = movement()
            vector.upd_angle(vector.a + vector.yaw)
            vector.get_cartesian()

            dr_mat = [0, 0, 0, 0]
            for i in range(4):
                dr_mat[i] = dr_mat[i] + mat[i] * offset[i]

            drone.send_rc_control(dr_mat[0], dr_mat[1], dr_mat[2], dr_mat[3])

            vector.graphing()
            print(dr_mat)
            display()
            time.sleep(0.05)

if __name__ == '__main__':
    main()