import cv2
import numpy as np
from collections import OrderedDict

cap = cv2.VideoCapture('vtest.mp4')

if cap.isOpened() == False:
    print("Error opening video")

backSub = cv2.createBackgroundSubtractorMOG2()

while cap.isOpened():
    ret, frame = cap.read()
    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    fgmask = backSub.apply(gray)
    
    # cv2.imshow('FG Mask', fgmask)
    shadowval = backSub.getShadowValue()
    ret, nmask = cv2.threshold(fgmask, shadowval, 255, cv2.THRESH_BINARY)
    cv2.imshow('Remove Shadow', nmask)
    
    height = nmask.shape[0]
    width = nmask.shape[1]
    cnt = 1
    equality = []
    equality_l = []
    equality_r = []
    cca = np.zeros((height,width))
    for i in range(height):
        for j in range(width):
            if nmask[i,j] == 255:
                if i > 0 and j + 1 < width and cca[i-1,j+1] != 0:
                    cca[i,j] = cca[i-1,j+1]
                    if cca[i,j-1] != 0 and j > 0:
                        equality_l.append(min(cca[i,j], cca[i,j-1]))
                        equality_r.append(max(cca[i,j-1], cca[i,j]))
                        for ele in equality:
                            if cca[i, j] in ele:
                                if cca[i, j-1] in ele:
                                    temp = 0 
                                else:
                                    ele.add(cca[i, j-1])
                            elif cca[i, j-1] in ele:
                                ele.add(cca[i,j])
                elif i > 0 and cca[i-1,j] != 0:
                    cca[i,j] = cca[i-1,j]
                elif i > 0 and j > 0 and cca[i-1,j-1] != 0:
                    cca[i,j] = cca[i-1,j-1]
                elif j > 0 and cca[i,j-1] != 0:
                    cca[i,j] = cca[i,j-1]
                else:
                    cca[i,j] = cnt
                    cnt += 1
    for a in range(6):
        for key, val in zip(equality_l, equality_r):
            cca[cca == key] = val
    boundingbox = dict()
    print(cca)
    for i in range(height):
        for j in range(width):
            if cca[i,j] in boundingbox:
                if boundingbox[cca[i, j]][1] < i:
                    boundingbox[cca[i,j]][1] = i
                if boundingbox[cca[i, j]][2] > j:
                    boundingbox[cca[i,j]][2] = j
                if boundingbox[cca[i, j]][3] < j:
                    boundingbox[cca[i,j]][3] = j
            else: 
                boundingbox[cca[i,j]] = [i, i, j, j]
    
    for key, val in boundingbox.items():
        if key == 0:
            continue
        if (val[3]-val[2])*(val[1]-val[0]) < 500:
            continue
        cv2.rectangle(frame, (val[2],val[0]), (val[3],val[1]), (255,0,0), 5)
    cv2.imshow("abc", frame)
    keyboard = cv2.waitKey(33)
    if keyboard == 27: # esc
        break

cap.release()
cv2.destroyAllWindows()