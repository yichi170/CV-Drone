# import tello
from djitellopy import Tello
import cv2
import numpy as np
import time
# from tello_control_ui import TelloUI
from pyimagesearch.pid import PID

filename = "out.xml"
textColor = (0, 225, 225)
textthickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1

def keyboard(self, key):
    #global is_flying
    print("key:", key)
    fb_speed = 40
    lf_speed = 40
    ud_speed = 50
    degree = 30
    if key == ord('1'):
        self.takeoff()
        #is_flying = True
    if key == ord('2'):
        self.land()
        #is_flying = False
    if key == ord('3'):
        self.send_rc_control(0, 0, 0, 0)
        print("stop!!!!")
    if key == ord('w'):
        self.send_rc_control(0, fb_speed, 0, 0)
        print("forward!!!!")
    if key == ord('s'):
        self.send_rc_control(0, (-1) * fb_speed, 0, 0)
        print("backward!!!!")
    if key == ord('a'):
        self.send_rc_control((-1) * lf_speed, 0, 0, 0)
        print("left!!!!")
    if key == ord('d'):
        self.send_rc_control(lf_speed, 0, 0, 0)
        print("right!!!!")
    if key == ord('z'):
        self.send_rc_control(0, 0, ud_speed, 0)
        print("down!!!!")
    if key == ord('x'):
        self.send_rc_control(0, 0, (-1) *ud_speed, 0)
        print("up!!!!")
    if key == ord('c'):
        self.send_rc_control(0, 0, 0, degree)
        print("rotate!!!!")
    if key == ord('v'):
        self.send_rc_control(0, 0, 0, (-1) *degree)
        print("counter rotate!!!!")
    if key == ord('5'):
        height = self.get_height()
        print(height)
    if key == ord('6'):
        battery = self.get_battery()
        print (battery)

def main():
    
    drone = Tello()
    drone.connect()

    time.sleep(10)

    print("breakpoint1")
    
    calib = cv2.FileStorage('out.xml',cv2.FILE_STORAGE_READ)
    intrinsic = calib.getNode("intrinsic").mat()
    distortion = calib.getNode("distortion").mat()

    print("breakpoint2")

    z_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
    y_pid = PID(kP=0.7, kI=0.0001, kD=0.1)
    yaw_pid = PID(kP=0.7, kI=0.0001, kD=0.1)

    yaw_pid.initialize()
    z_pid.initialize()
    y_pid.initialize()

    print("breakpoint3")

    while True:
        frame = drone.get_frame_read()
        print("breakpoint4")
        frame = frame.frame
        frame2 = frame.copy()

        dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters_create()
        markerConers, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame2, dictionary, parameters=parameters)
        frame2 = cv2.aruco.drawDetectedMarkers(frame2, markerConers, markerIds)
        rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerConers, 15, intrinsic, distortion)
        print(rvec)
        print(tvec)
        print(_objPoints)
        if rvec is not None and tvec is not None:
            frame2 = cv2.aruco.drawAxis(frame2, intrinsic, distortion, rvec, tvec, 5)
            frame2 = cv2.putText(frame2, 
                    f'x: {tvec[0][0][0]:.2f} y: {tvec[0][0][1]:.2f} z: {tvec[0][0][2]:.2f}',
                    (00, 185), font, fontScale, textColor, textthickness, cv2.LINE_AA, False)


        cv2.imshow("drone", frame2) 
        key = cv2.waitKey(33)

        if key != -1:
            drone.keyboard(key)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
