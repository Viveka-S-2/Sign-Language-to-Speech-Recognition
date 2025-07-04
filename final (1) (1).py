import numpy as np
import track_hand as htm
import time
import cv2
import urllib.request
import requests

# ESP32-CAM URL for image capture
url = "http://192.168.208.197/cam-lo.jpg"  # Update this with the actual IP address from Serial Monitor

# ESP32 server URL for receiving ASL letters
esp32_url = "http://192.168.208.197/letter"  # Update this with the actual IP address from Serial Monitor

wCam, hCam = 800, 600

detector = htm.handDetector(maxHands=1)

def recognizeASL(fingers):
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

try:
    while True:
        fingers = [0, 0, 0, 0, 0]

        print("Capturing image from ESP32-CAM...")
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if lmList:
            fingers = detector.fingersUp()
            asl_letter = recognizeASL(fingers)
            
            print(f"Detected ASL letter: {asl_letter}")

            if asl_letter != 'Unknown':
                # Send the ASL letter to the ESP32 server
                try:
                    response = requests.post(esp32_url, data={'letter': asl_letter})
                    print(f"Sent letter '{asl_letter}' to ESP32, response: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Failed to send data to ESP32: {e}")
                
                cv2.putText(img, asl_letter, (bbox[0], bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
