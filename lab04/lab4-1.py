import cv2
import numpy as np

filename = "out.xml"
nx = 9
ny = 6
cap = cv2.VideoCapture(2)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
objpoints = []
imgpoints = []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    ret, frame = cap.read()
    if len(objpoints) == 5:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)
    if ret == True:
        # print('ok')
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

    
    cv2.drawChessboardCorners(frame, (nx, ny), corners, ret)
    cv2.imshow('frame', frame)
    # cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1))
    # cv2.imshow('frame', frame)
    k = cv2.waitKey(33)
    if k == 27:
        break

# print('out1')
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# print('out2')
f = cv2.FileStorage(filename, cv2.FILE_STORAGE_WRITE)
f.write("intrinsic", mtx)
f.write("distortion", dist)
f.release()
# print(mtx,dist)