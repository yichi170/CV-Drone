import cv2
import numpy as np

def gray_mean(stat, T):
    cnt1, cnt2 = 0, 0
    for i in range(T):
        cnt1 += i * stat[i]
    cnt1 /= np.sum(stat[ : T])
    for i in range(T, 256):
        cnt2 += i * stat[i]
    cnt2 /= np.sum(stat[T : ])
    return cnt1, cnt2

def OTSU(stat, T):
    W0 = np.sum(stat[ : T]) / np.sum(stat)
    W1 = np.sum(stat[T : ]) / np.sum(stat)
    U0, U1 = gray_mean(stat, T)
    return W0 * W1 * ((U0 - U1) ** 2)

image = cv2.imread('input.jpg',cv2.IMREAD_GRAYSCALE)
stat = np.zeros(256).tolist()
for i in image:
    for j in i:
        stat[j] += 1

temp = 0
idx = 0
for i in range(254):
    otsu = OTSU(stat,i)
    if temp < otsu:
        idx = i
    temp = max(temp,otsu)
    print("--out-- : ",i,otsu)

print(idx)

for i, _ in enumerate(image):
    for j, k in enumerate(_):
        if k >= idx:
            image[i][j] = 255
        else:
            image[i][j] = 0

cv2.imshow("Lab2-2", image)
cv2.waitKey(0)
