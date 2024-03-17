import cv2
import numpy as np
import time
import os
import pytesseract
import handtrackingmodule as htm
import mediapipe as mp
from PIL import ImageGrab


pTime = 0
brushThickness = 15
eraserThickness = 50

shape = 'freestyle'

folderPath = "Header"
myList = os.listdir(folderPath)
#print(myList)
overlaylist = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlaylist.append(image)
#print(len(overlaylist))
header = overlaylist[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = htm.handDetector(detectionCon=0.85)
#detection = ocr.findocr()
xp,yp =0, 0
imgCanvas = np.zeros((720,1280,3),np.uint8)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

res = cv2.VideoWriter('filename.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
v1 = 0
v2 = 0
hypothesis = "NONE"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  

while True:
    hypothesis = "NONE"
    #1.import the image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    #2.find hand landmarks
    img = detector.findHands(img, draw=False)
    lmlist = detector.findPosition(img, draw=False)
    
    res.write(img)
    
    if len(lmlist)!=0:
        #print(lmlist) 
        #tip of index and middle finger
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        x0, y0 = lmlist[4][1:]

        #3.check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)

        #4.if selection mode - two fingers are up 
        if fingers[1] and fingers[2]:
            xp,yp =0, 0
            #print("Selection Mode")
            if y1 < 125 :
                if 0<x1<125:
                    header = overlaylist[4]
                    drawColor = (0, 0, 255)
                    shape = 'circle'
                elif 240<x1<350:
                    header = overlaylist[5]
                    drawColor = (0,0,255)
                    shape = 'rectangle'
                elif 500<x1<600:
                    header = overlaylist[0]
                    drawColor = (255, 0, 255)
                    shape = 'freestyle'
                elif 700<x1<800:
                    header = overlaylist[2]
                    drawColor = (0, 255, 0)
                    shape = 'freestyle'
                elif 900<x1<1000:
                    header = overlaylist[1]
                    drawColor = (255, 0, 0)
                    shape = 'freestyle'
                elif 1100<x1<1200:
                    header = overlaylist[3]
                    drawColor = (0 , 0, 0)
                    shape = 'freestyle'
            cv2.rectangle(img, (x1,y1-25), (x2,y2+25),drawColor, cv2.FILLED)
            #cv2.rectangle(imgCanvas, (x1,y1-25), (x2,y2+25),drawColor, cv2.FILLED)
            #cv2.rectangle(imgInv, (x1,y1-25), (x2,y2+25), cv2.FILLED)
       
        #5.if drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            #print("Drawing Mode")
            if xp==0 and yp==0 :
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                eraserThickness = 50
                z1, z2 = lmlist[4][1:]
                result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                    # print(result)
                if result < 0:
                    result = -1 * result
                u = result
                if fingers[1] and fingers[4]:
                        eraserThickness = u
                cv2.line(img, (xp,yp), (x1,y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp,yp), (x1,y1), drawColor, eraserThickness)
            else :
                if shape == 'freestyle':
                        z1, z2 = lmlist[4][1:]
                        
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        # print(result)
                        if result < 0:
                            result = -1 * result
                        u = result

                        cv2.line(img, (xp,yp), (x1,y1), drawColor, brushThickness)
                        cv2.line(imgCanvas, (xp,yp), (x1,y1), drawColor, brushThickness)
                if shape == 'circle':
                        z1, z2 = lmlist[4][1:]
                        # print(z1,z2)
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        # print(result)
                        if result < 0:
                            result = -1 * result
                        u = result
                        #cv2.putText(img, "Radius Of Circle = ", (0, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        #cv2.putText(img, str(u), (450, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        cv2.circle(img,(x0,y0),u,drawColor)
                        if fingers[4]:
                            if v1 == 24 :
                                cv2.circle(imgCanvas, (x0, y0), u, drawColor)
                                print("circle with radius = ",str(u))
                                v1=0
                            v1+=1
                if shape == 'rectangle':
                        z1, z2 = lmlist[4][1:]
                        # print(z1,z2)
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        # print(result)
                        if result < 0:
                            result = -1 * result
                        u = result
                        cv2.rectangle(img, (x0, y0), (x1, y1), drawColor)
                        #cv2.putText(img, "Length of Diagonal = ", (0, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        #cv2.putText(img, str(u), (530, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        if fingers[4]:
                            if v2 == 24 :
                                cv2.rectangle(imgCanvas, (x0, y0), (x1, y1), drawColor)
                                print("rectangle with diagonal length = ",str(u))
                                cv2.circle
                                v2 = 0
                            v2+=1
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    #imgInv = cv2.bitwise_and(imgInv,img)
    img = cv2.bitwise_or(img,imgCanvas)

    #setting the header image
    img[0:125,0:1280] = header
    #imgInv[0:125,0:1280] = header
    #imgCanvas[0:125,0:1280] = header

    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    #imgInv = cv2.addWeighted(img,0.2,imgInv,0.7,0)
    
    #cv2.imshow("Canvas",imgCanvas)
    #cv2.imshow("Inv",imgInv)
    #cv2.imshow("GrayScale",imgGray)

    # 11. Frame Rate
    cTime = time.time()
    fps1 = 1 / (cTime - pTime)
    fps2 = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {str(int(fps1))}' , (20, 700), cv2.FONT_HERSHEY_PLAIN, 2,(0, 0, 255), 2)

    cv2.imshow("Air Writing",img)

    key = cv2.waitKey(1)
    if key == ord('q'): 
        break
    if key == ord('s'):
        cv2.imshow("Inv",imgInv)
        pic = ImageGrab.grab(bbox=(10,10,1600,930))
        pic.save("image.png")
        hypothesis4 = pytesseract.image_to_string("image.png", lang="eng")
        print("                       ")
        print("Character Recognized : ")
        print(hypothesis4) 
    if key == ord('c'):
         cv2.destroyWindow("Inv")
# Release the video capture object and clean up

res.release()
cap.release()
cv2.destroyAllWindows()
