import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

img1 = cv2.imread('pic4.jpg')
img1 = cv2.resize(img1,(img1.shape[1]//4,img1.shape[0]//4),interpolation=cv2.INTER_CUBIC)
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

img2 = cv2.imread('pic6.jpg')
img2 = cv2.resize(img2,(img2.shape[1]//4,img2.shape[0]//4),interpolation=cv2.INTER_CUBIC)
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

start = time.time()
# detector = cv2.xfeatures2d.SURF_create()
# detector = cv2.xfeatures2d.SIFT_create()
detector = cv2.ORB_create()

kp1, des1 = detector.detectAndCompute(gray1, None)
kp2, des2 = detector.detectAndCompute(gray2, None)

print(time.time() - start)
# for orb
# bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
# print(type(des1[0,0]))
# matches = bf.match(des1,des2)
# matches = sorted(matches, key=lambda x:x.distance)

# img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# print(time.time() - start)
# cv2.imshow('img',img3)
# cv2.waitKey(0)
# cv2.imwrite('orb45.png',img3)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)
print(len(matches))
good = []
for m,n in matches:
    if m.distance < 0.5*n.distance:
        good.append([m])
print(len(good))

img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1],3), dtype=np.uint8)
print(time.time() - start)
cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,img_matches)
cv2.imshow('matches',img_matches)
cv2.waitKey(0)
cv2.imwrite('orb46.png',img_matches)