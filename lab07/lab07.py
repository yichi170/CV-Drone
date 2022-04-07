# import tello
from djitellopy import Tello
import cv2
import numpy as np
import time
import math
from pyimagesearch.pid import PID
import os

filename = "out.xml"
textColor = (0, 225, 225)
textthickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
max_speed_threshold = 40

def keyboard(drone, key):
    print("key:", key)
    fb_speed = 40
    lf_speed = 40
    ud_speed = 50
    degree = 30
    if key == ord('1'):
        drone.takeoff()
    if key == ord('2'):
        drone.land()
    if key == ord('3'):
        drone.send_rc_control(0, 0, 0, 0)
        print("stop!!!!")
    if key == ord('w'):
        drone.send_rc_control(0, fb_speed, 0, 0)
        print("forward!!!!")
    if key == ord('s'):
        drone.send_rc_control(0, (-1) * fb_speed, 0, 0)
        print("backward!!!!")
    if key == ord('a'):
        drone.send_rc_control((-1) * lf_speed, 0, 0, 0)
        print("left!!!!")
    if key == ord('d'):
        drone.send_rc_control(lf_speed, 0, 0, 0)
        print("right!!!!")
    if key == ord('z'):
        drone.send_rc_control(0, 0, ud_speed, 0)
        print("down!!!!")
    if key == ord('x'):
        drone.send_rc_control(0, 0, (-1) *ud_speed, 0)
        print("up!!!!")
    if key == ord('c'):
        drone.send_rc_control(0, 0, 0, degree)
        print("rotate!!!!")
    if key == ord('v'):
        drone.send_rc_control(0, 0, 0, (-1) *degree)
        print("counter rotate!!!!")
    if key == ord('5'):
        height = drone.get_height()
        print(height)
    if key == ord('6'):
        battery = drone.get_battery()
        print (battery)

def clip_val(val):
    if val > max_speed_threshold:
        val = max_speed_threshold
    elif val < -max_speed_threshold:
        val = -max_speed_threshold
    return val

def follow(drone, tvec, rvec, z_pid, y_pid, yaw_pid):
    z_update = tvec[0, 0, 2] - 100
    print("org_z: " + str(z_update))
    z_update = z_pid.update(z_update, sleep=0)
    print("pid_z: " + str(z_update))
    z_update = clip_val(z_update)
    # drone.send_rc_control(0, int(z_update // 2), 0, 0)

    y_update = tvec[0, 0, 1] - 8
    print("org_y: " + str(y_update))
    y_update = clip_val(y_update)
    y_update = y_pid.update(y_update, sleep=0) - 8
    print("pid_y: " + str(y_update))
    y_update = clip_val(y_update)
    y_update *= 2.5
    z_update *= 1

    dst, jaco = cv2.Rodrigues(rvec[0][0])
    z_ = np.array([dst[0][2], dst[1][2], dst[2][2]])
    v = np.array([z_[0], 0, z_[2]])
    degree = math.atan2(z_[2], z_[0])
    degree = -degree * 180 / math.pi
    print("ori_degree: ", degree)
    degree -= 85
    if degree > 20:
        degree = 20
    elif degree < -20:
        degree = -20
    else:
        degree = 0

    print("after degree: ", degree)
    drone.send_rc_control(0, int(z_update // 2), int(-y_update // 2), int(degree))
    if int(degree) > 0:
        print("right")
    elif int(degree) < 0:
        print("left")

def goleft(drone, tvec, rvec, z_pid, y_pid, yaw_pid):
    pass
def main():
    
    drone = Tello()
    drone.connect()

    time.sleep(13)

    print("breakpoint1")
    
    calib = cv2.FileStorage('out.xml',cv2.FILE_STORAGE_READ)
    intrinsic = calib.getNode("intrinsic").mat()
    distortion = calib.getNode("distortion").mat()

    print("breakpoint2")

    z_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
    y_pid = PID(kP=1.0, kI=0.0001, kD=0.1)
    yaw_pid = PID(kP=0.7, kI=0.0001, kD=0.1)

    yaw_pid.initialize()
    z_pid.initialize()
    y_pid.initialize()

    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    print("breakpoint3")
    
    drone.streamon()

    while True:
        frame = drone.get_frame_read()
        frame = frame.frame
        frame2 = frame.copy()

        markerConers, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame2, dictionary, parameters=parameters)
        frame2 = cv2.aruco.drawDetectedMarkers(frame2, markerConers, markerIds)
        rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerConers, 15, intrinsic, distortion)

        key = cv2.waitKey(33)

        if key != -1:
            keyboard(drone, key)

        if rvec is not None and tvec is not None:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Marker ID: ", markerIds)
            
            if markerIds == 0:
                follow(drone, tvec, rvec, z_pid, y_pid, yaw_pid)
            elif markerIds == 5:
                goleft(drone, tvec, rvec, z_pid, y_pid, yaw_pid)
            elif markerIds == 3:
                goright(drone, tvec, rvec, z_pid, y_pid, yaw_pid)

            # drone.send_rc_control(0, int(z_update // 2), int(-y_update // 2), int(degree))
        else:
            drone.send_rc_control(0, 0, 0, 0)

        cv2.imshow("drone", frame2) 
        key = cv2.waitKey(33)

        if key != -1:
            keyboard(drone, key)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
