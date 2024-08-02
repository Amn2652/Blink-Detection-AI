import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import os

video_capture = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

leftEyeIDList = [362, 382, 381, 380, 374, 373, 390, 249, 466, 387, 386, 385, 384, 398]
rightEyeIDList = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

leftRatioList = []
rightRatioList = []
counter = 0

def send_scroll_command():
    os.system("adb shell input swipe 250 800 250 400 100")

while True:
    success, img = video_capture.read()
    
    if not success:
        break
    
    img, faces = detector.findFaceMesh(img, draw=False)
    if faces:
        face = faces[0]
        
        leftUp = face[386]
        leftDown = face[374]
        leftLeft = face[362]
        leftRight = face[263]
        lengthVerLeft, _ = detector.findDistance(leftUp, leftDown)
        lengthHorLeft, _ = detector.findDistance(leftLeft, leftRight)
        ratioLeft = (lengthVerLeft / lengthHorLeft) * 100
        leftRatioList.append(ratioLeft)
        if len(leftRatioList) > 3:
            leftRatioList.pop(0)
        ratioAvgLeft = sum(leftRatioList) / len(leftRatioList)
        if ratioAvgLeft < 23:
            print("Blink (Left Eye)")
            send_scroll_command()
        
        rightUp = face[159]
        rightDown = face[145]
        rightLeft = face[33]
        rightRight = face[133]
        lengthVerRight, _ = detector.findDistance(rightUp, rightDown)
        lengthHorRight, _ = detector.findDistance(rightLeft, rightRight)
        ratioRight = (lengthVerRight / lengthHorRight) * 100
        rightRatioList.append(ratioRight)
        if len(rightRatioList) > 3:
            rightRatioList.pop(0)
        ratioAvgRight = sum(rightRatioList) / len(rightRatioList)
        if ratioAvgRight < 23 and counter == 0:
            print("Blink (Right Eye)")
            send_scroll_command()
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 20:
                counter = 0
        
    cv2.imshow("Display", img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
