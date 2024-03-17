import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplexity=1,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self,img,draw=True):

        imgRGB  =cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks :
            for handLms in self.results.multi_hand_landmarks :
                if draw :
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img 

    def findPosition(self, img, handNO=0, draw=True):  

        self.lmlist = []
        if self.results.multi_hand_landmarks :
            myHand = self.results.multi_hand_landmarks[handNO]
            for id,lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,m,c = img.shape
                cx,cy = int(lm.x*m),int(lm.y*h)
                #print(id,cx,cy)
                self.lmlist.append([id, cx, cy])
                if draw :
                    cv2.circle(img,(cx,cy),7,(255,0,0),cv2.FILLED)
        return self.lmlist
    
    def fingersUp(self):
        fingers = []

        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else :
            fingers.append(0)

        for id in range(1, 5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
        

def main():
    pTime = 0 
    cTime = 0

    cap = cv2.VideoCapture(0)

    detector = handDetector()
    while True :
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList)!=0:
           print(lmList)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cv2.imshow("Image",img)
        cv2.waitKey(1)

if __name__ == "__main__":
     main()