import cv2
import time
import track_hand as htm
import pyttsx3
import requests
import numpy as np

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize hand detector
detector = htm.handDetector(maxHands=1)

# Track letters to form words
sentence = ""
asl_letter = ""
last_letter = ""
last_time = time.time()
cooldown = 1.0  # seconds between new letter updates

# ESP32-CAM stream URL
esp32_url = "http://192.168.208.197/cam-lo.jpg"

# Set window properties (bigger and resizable)
cv2.namedWindow("ASL Recognition (ESP32-CAM)", cv2.WINDOW_NORMAL)
cv2.resizeWindow("ASL Recognition (ESP32-CAM)", 960, 720)  # Adjust as needed

while True:
    try:
        # Fetch frame from ESP32-CAM
        img_resp = requests.get(esp32_url, timeout=2)
        img_array = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f" Error fetching image from ESP32-CAM: {e}")
        continue

    if img is None:
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    current_time = time.time()

    if lmList:
        fingers = detector.fingersUp()
        detected_letter = htm.recognizeASL(fingers)

        # Only update current displayed letter if cooldown passed and it's not Unknown
        if detected_letter != "Unknown" and (detected_letter != last_letter or (current_time - last_time > cooldown)):
            asl_letter = detected_letter
            last_letter = detected_letter
            last_time = current_time

        # Show the current potential letter
        if bbox:
            cv2.putText(img, f"{asl_letter}", (bbox[0], bbox[1] - 30),
                        cv2.FONT_HERSHEY_PLAIN, 2.5, (255, 0, 255), 2)

    # Display full sentence
    cv2.putText(img, f"Text: {sentence}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(img, "Press 'Enter'=Add | 'Space'=Space | 'Backspace'=Delete", (10, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 255), 2)
    cv2.putText(img, "Press 's'=Speak | 'c'=Clear | 'q'=Quit", (10, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 255), 2)

    cv2.imshow("ASL Recognition (ESP32-CAM)", img)
    key = cv2.waitKey(1) & 0xFF

    if key == 13:  # Enter key
        if asl_letter and asl_letter != "Unknown":
            sentence += asl_letter

    elif key == 32:  # Space key
        sentence += " "

    elif key == 8:  # Backspace key
        sentence = sentence[:-1]

    elif key == ord('s'):
        if sentence:
            engine.say(sentence)
            engine.runAndWait()

    elif key == ord('c'):
        sentence = ""
        asl_letter = ""
        last_letter = ""
        last_time = time.time()

    elif key == ord('q'):
        break

cv2.destroyAllWindows()
