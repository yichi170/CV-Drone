import cv2

cap = cv2.VideoCapture('test_video.MOV')

if cap.isOpened():
    rval, frame = cap.read()
else:
    exit()
count = 0
with open('rgb.txt','w') as f:
    while rval:
        rval, frame = cap.read()
        # cv2.imshow('frame',frame)
        # cv2.waitKey(33)
        if rval and count%4==0:
            frame = cv2.resize(frame,(640,480))
            cv2.imwrite(f"images/{count//4:04d}.jpg",frame)
            f.write(f"{count//4} rgb/{count//4:04d}.jpg\n")
        count += 1
print(count)
