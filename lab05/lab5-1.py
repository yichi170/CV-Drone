import cv2
import numpy as np
import xml.etree.ElementTree as XET

calib = cv2.FileStorage('out.xml',cv2.FILE_STORAGE_READ)
intrinsic = calib.getNode("intrinsic").mat()
distortion = calib.getNode("distortion").mat()
print(intrinsic)
print(distortion)

# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

#     parameters = cv2.aruco.DetectorParameters_create()

#     markerCorners, markerlds, rejectedCandidates = cv2.aruco.detectMarkers(frame,dictionary,parameters=parameters)
#     frame = cv2.aruco.drawDetectedMarkers(frame,markerCorners,markerlds)

#     rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 15, intrinsic, distortion)
#     if rvec is not None and tvec is not None:
#         frame = cv2.aruco.drawAxis(frame,intrinsic,distortion,rvec,tvec,0.1)

#     cv2.imshow('frame', frame)
#     k = cv2.waitKey(33)
#     if k == 27:
#         break