import cv2
import numpy as np

image = cv2.imread('kifune.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
image2 = np.zeros(image.shape,np.float64)
image2 = image

distr = np.zeros(256)
for i in range(hsv.shape[0]):
    for j in range(hsv.shape[1]):
        distr[hsv[i,j,2]] += 1

accum = np.zeros(256)
for i in range(256):
    accum[i] = distr[0:i+1].sum()

accum /= accum.max()
trans = accum * 255
for i in range(hsv.shape[0]):
    for j in range(hsv.shape[1]):
        hsv[i,j,2] = trans[hsv[i,j,2]]

bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imshow('Lab2-1b', bgr)
cv2.waitKey(0)

# ===================

distrBGR = np.zeros((3, 256))
for i in range(image2.shape[0]):
    for j in range(image2.shape[1]):
        for c in range(3):
            distrBGR[c, image2[i,j,c]] += 1
# print(distrBGR)
accumBGR = np.zeros((3,256))
for i in range(256):
    for c in range(3):
        accumBGR[c,i] = distrBGR[c,0:i+1].sum()
for c in range(3):
    accumBGR[c] /= accumBGR[c].max()
trans = accumBGR * 255
for i in range(image2.shape[0]):
    for j in range(image2.shape[1]):
        for c in range(3):
            image2[i,j,c] = trans[c,image2[i,j,c]]
print(image2)
# bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imshow('Lab2-1a', image2)
cv2.waitKey(0)
