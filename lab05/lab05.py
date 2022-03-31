import tello
import cv2
import numpy as np
import time
from tello_control_ui import TelloUI

filename = "out.xml"
textColor = (0, 225, 225)
textthickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1

def main():

    nx = 9
    ny = 6
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    objpoints = []
    imgpoints = []
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    drone = tello.Tello('', 8889)      
    time.sleep(10)
    
    while True:
        frame = drone.read()
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if len(objpoints) == 5:
            break
        frame2 = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)
        
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)

            # cv2.drawChessboardCorners(frame, (nx, ny), corners, ret)
        cv2.imshow("drone", bgr)
        key = cv2.waitKey(33)

        if key != -1:
            drone.keyboard(key)
    
    ret, intrinsic, distortion, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    f = cv2.FileStorage(filename, cv2.FILE_STORAGE_WRITE)
    f.write("intrinsic", intrinsic)
    f.write("distortion", distortion)
    f.release()
    print('calibration done')

    while True:
        frame = drone.read()
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame2 = bgr.copy()

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
