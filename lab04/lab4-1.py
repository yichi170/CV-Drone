import cv2

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, )

    if ret == True:
        

    cv2.imshow('frame', frame)
    cv2.waitKey(33)