import cv2
import numpy as np

frame = cv2.imread('broadway.jpg')
height, width = frame.shape[:2]
print(height, width)
# cv2.imshow('frame', frame)
# cv2.waitKey(0)
# cv2.getPerspectiveTransform()

cap = cv2.VideoCapture(0)

while True:
    ret, cam = cap.read()
    if ret == False:
        break
    
    camheight, camwidth = cam.shape[:2]
    
    out_frame = np.copy(frame)
    
    src = np.float32([[0, 0], [camwidth -1, 0], [camwidth - 1,camheight - 1], [0, camheight - 1]])
    dst = np.float32([[202, 422], [426, 423], [421, 631], [99, 611]])
    dst = np.float32([[422, 202], [426, 423], [631, 421], [611, 101]])
    # dst = src/2 +200
    pmat = cv2.getPerspectiveTransform(src, dst)
    # print(pmat)
    # warped = cv2.warpPerspective(cam, pmat, (width, height))

    for i in range(cam.shape[0]):
        for j in range(cam.shape[1]):
            trans = np.dot(pmat, np.array([i, j, 1]))/np.dot(pmat, np.array([i, j, 1]))[2]
            # trans = np.matmul(pmat, np.array([i, j, 1]))
            out_frame[trans[0].astype(int),trans[1].astype(int)] = cam[i,j]
    cv2.imshow('frame2', out_frame)
    cv2.waitKey(33)
    # print(warped.shape)