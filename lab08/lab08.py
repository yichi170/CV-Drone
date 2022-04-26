import cv2
import dlib
import numpy as np

# human detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# face detector
detector = dlib.get_frontal_face_detector()

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('../lab03/vtest.mp4')
calib = cv2.FileStorage('out.xml',cv2.FILE_STORAGE_READ)
intrinsic = calib.getNode("intrinsic").mat()
distortion = calib.getNode("distortion").mat()

fw = 14 / 2 # face width / 2
face_3d = np.array([(-fw,-fw,0.0),(-fw,fw,0.0),(fw,-fw,0.0),(fw,fw,0.0)])

hw = 100 / 2 # human width / 2
hh = 200 / 2 # human height / 2
human_3d = np.array([(-hw,-hh,0.0),(-hw,hh,0.0),(hw,-hh,0.0),(hw,hh,0.0)])

while True:
    ret, cam = cap.read()
    if ret == False:
        break

    human_rects, weights = hog.detectMultiScale(cam,winStride=(6,6),scale=1.25,useMeanshiftGrouping=False)

    face_rects = detector(cam,0)

    for (x,y,w,h) in human_rects:
        cv2.rectangle(cam,(x,y),(x+w,y+h),(0,255,0),3)

        human_2d = np.array([(x,y),(x,y+h),(x+w,y),(x+w,y+h)],dtype=np.float32)
        success, rvec, tvec = cv2.solvePnP(human_3d,human_2d,intrinsic,distortion)
        if success:
            cv2.putText(cam,str(tvec[2,0]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,192,0),2,cv2.LINE_AA)

    for d in face_rects:
        x1 = d.left()
        y1 = d.top()
        x2 = d.right()
        y2 = d.bottom()
        cv2.rectangle(cam,(x1,y1),(x2,y2),(255,0,0),3)

        face_2d = np.array([(x1,y1),(x1,y2),(x2,y1),(x2,y2)],dtype=np.float32)
        success, rvec, tvec = cv2.solvePnP(face_3d,face_2d,intrinsic,distortion)
        if success:
            cv2.putText(cam,str(tvec[2,0]),(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(192,0,0),2,cv2.LINE_AA)
    
    cv2.imshow('frame',cam)
    k = cv2.waitKey(1)
    if k == 27:
        break
