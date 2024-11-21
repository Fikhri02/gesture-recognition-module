import cv2
import mediapipe as mp
import time
import os
import main as htm
import socket

wCam, hCam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)



mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


detector = htm.handDetector(detectionCon=0.75)
tipIds = [4,8,12,16,20]

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
machine = socket.gethostbyname(socket.gethostname())
port = 9999

client.connect((machine,port))
def receiver():
    pTime = 0
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        #print(lmList)

        if len(lmList)!=0:

            fingers = []
            #Thumbif
            if lmList[2][1] > lmList[17][1]:
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # print(fingers)
                totalFingers = fingers.count(1)
                #print(totalFingers)
            else:
                print("8")

        else:
            print("7")


        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        img2 = cv2.flip(img, 1)
        cv2.putText(img, f'FPS:{int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)
        cv2.imshow("Image",img2)
        cv2.waitKey(1)
        if len(lmList)!=0 :
            if lmList[tipIds[2]][1] > lmList[17][1]:
                res = bytes(str(totalFingers), 'utf-8')
            else:
                res=bytes("8",'utf-8')
        else :
            res = bytes("7", 'utf-8')
        client.send(res)
        data = client.recv(1024)
        data2 = data.decode('UTF-8')
        print(data2)

receiver()