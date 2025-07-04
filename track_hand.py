import cv2
import mediapipe as mp
import time
import math
import numpy as np

class handDetector:
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

def recognizeASL(fingers):
    # Define a basic dictionary of finger configurations for the ASL alphabet
    asl_signs = {
       (0, 0, 0, 0, 0): 'A',  # Only thumb up.
        (0, 1, 1, 1, 1): 'B',  # All fingers up except thumb.
        (1, 1, 1, 1, 0): 'C',  # Only pinky down.
        (0, 0, 1, 0, 1): 'D',  # middle and pinky up.
        (0, 0, 0, 0, 1): 'E',  # only pinky up.
        (1, 0, 1, 1, 1): 'F',  # Only index down.
        (0, 0, 1, 1, 1): 'G',  # Thumb and index down.
        (0, 1, 0, 0, 1): 'H',  # index and pinky up.
        (0, 1, 1, 0, 0): 'I',  # middle index up.
        (0, 1, 0, 1, 0): 'J',  # index ring up.
        (0, 1, 0, 0, 0): 'K',  # Only index up.
        (0, 0, 0, 1, 1): 'L',  # ring and pinky up.
        (1, 0, 1, 0, 0): 'M',  # middle finger rev.
        (0, 0, 1, 0, 0): 'N',  # middle finger.
        (1, 0, 0, 0, 1): 'O',  # Thumb pinky up.
        (1, 1, 1, 0, 0): 'P',  # pinky and ring down.
        (0, 1, 1, 0, 1): 'Q',  # ring thumb down.
        (1, 0, 1, 0, 1): 'R',  # Only index and ring down.
        (0, 1, 0, 1, 1): 'S',  # thumb middle down.
        (1, 1, 0, 0, 1): 'T',  # thumb index and pinky up.
        (0, 1, 1, 1, 0): 'U',  # Thumb and pinky down.
        (1, 1, 1, 1, 1): 'V',  # All fingers up.
        (1, 0, 0, 0, 0): 'W',  # Only thumb up and tilted.
        (1, 1, 0, 1, 1): 'X',  # Only middle down.
        (0, 0, 1, 1, 0): 'Y',  # ring and middle up.
        (1, 0, 0, 1, 1): 'Z'   # index and middle down.
    }
    return asl_signs.get(tuple(fingers), 'Unknown')

def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        
        if lmList:
            fingers = detector.fingersUp()
            asl_letter = recognizeASL(fingers)
            cv2.putText(img, asl_letter, (bbox[0], bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        cv2.imshow("Image", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

