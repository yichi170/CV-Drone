import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.mp4')
cap.isOpened()
backSub = cv2.createBackgroundSubtractorMOG2()

def prune(cor):
    if (cor[0] - cor[1]) * (cor[2] - cor[3]) <= 5000:
        return True

class TWO_P():
    def __init__(self,mask):
        self.set = []
        self.set_cnt = 0
        self.label = np.zeros(mask.shape,dtype=np.int8).tolist()
        self.mask = mask
        self.lb_cnt = 1

    def find(self,p):
        if self.set[p-1] < 0:
            return p
        self.set[p-1] = self.find(self.set[p-1])
        return self.set[p-1]
    def union(self,p,q):
        proot = self.find(p)
        qroot = self.find(q)
        if proot == qroot:
            return
        elif self.set[proot-1] > self.set[qroot-1]:
            self.set[qroot-1] += self.set[proot-1]
            self.set[proot-1] = qroot
        else:
            self.set[proot-1] += self.set[qroot-1]
            self.set[qroot-1] = proot
        self.set_cnt -= 1
    def is_connected(self,p,q):
        if p == 0 or q == 0:
            return True
        return self.find(p) == self.find(q)

    def check(self,i,j):
        if i != 0 and self.label[i-1][j] != 0:
            self.label[i][j] = self.label[i-1][j]
        elif j != 0 and self.label[i][j-1] != 0:
            self.label[i][j] = self.label[i][j-1]
        else:
            self.label[i][j] = self.lb_cnt
            self.set.append(-1)
            self.set_cnt += 1
            self.lb_cnt += 1
        if self.label[i-1][j] != self.label[i][j-1] and self.is_connected(self.label[i-1][j],self.label[i][j-1]) == False:
            self.union(self.label[i-1][j],self.label[i][j-1])
        
    def two_pass(self):
        lb_set = []
        obj = {} # obj[label] = [max_i,min_i,max_j,min_j]
        
        for i,m1 in enumerate(self.mask):
            for j,m2 in enumerate(m1):
                if m2 == 255:
                    self.check(i,j)

        for i,l1 in enumerate(self.label):
            for j,l2 in enumerate(l1):
                if l2 != 0:
                    self.label[i][j] = self.find(self.label[i][j])

        for i,l1 in enumerate(self.label):
            for j,l2 in enumerate(l1):
                if l2 != 0:
                    obj.setdefault(l2,[0,self.mask.shape[0],0,self.mask.shape[1]])
                    obj[l2][0] = max(i,obj[l2][0])
                    obj[l2][1] = min(i,obj[l2][1])
                    obj[l2][2] = max(j,obj[l2][2])
                    obj[l2][3] = min(j,obj[l2][3])

        # print(self.label)
        prune_i = []
        for i in obj:
            if prune(obj[i]):
                prune_i.append(i)
        for i in prune_i:
            obj.pop(i)

        return obj


while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask  = backSub.apply(gray)
    shadowval = backSub.getShadowValue()
    ret, nmask = cv2.threshold(fgmask, shadowval, 255, cv2.THRESH_BINARY)
    handler = TWO_P(nmask)
    obj = handler.two_pass()
    print('obj :',obj)
    # print(nmask)
    for i in obj:
        cv2.rectangle(frame,(obj[i][3],obj[i][1]),(obj[i][2],obj[i][0]),(255,0,0),5)
    # print(frame.shape)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(33)
    if k == 27:
        break