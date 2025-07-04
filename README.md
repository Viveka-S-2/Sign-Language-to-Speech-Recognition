The goal is to create a low-cost, real-time system for recognizing and interpreting hand movements in Sign Language (SL) by using Python-based computer vision libraries and the ESP32-CAM microcontroller. With the use of an offline text-to-speech engine pyttsx3, the identified gestures will be converted from text to speech. This system is intended to provide a portable, embedded, and accessible solution that will enable smooth and effective communication for those with speech and hearing impairments.

The ESP32-CAM microcontroller will be used to construct a real-time hand gesture recognition system.

•	using MediaPipe and OpenCV to identify hand motions.
•	to translate static ASL commands into text.
•	Using pyttsx3, turn detected text into speech.
•	in order to guarantee real-time feedback and offline operation.
•	to encourage inclusive and easily obtainable communication ways.

Components Used

•	The image capture unit is the ESP32-CAM microcontroller. It has a built-in camera and a Wi-Fi module for live image streaming.
•	The FTDI Programmer is used to set up the ESP32-CAM's Wi-Fi settings and upload the Arduino sketch to it.
•	Wi-Fi Network: Enables the ESP32-CAM to send picture frames to the host PC.
•	Host PC: Utilizes the Python backend to generate text, process images, detect hand gestures, and produce speech.

Software and Libraries

•	The Arduino IDE is used to program an image streaming sketch for the ESP32-CAM. It manages camera setup and web server setup.
•	ESP32-CAM video frames can be retrieved, preprocessed, and managed using OpenCV, a Python computer vision library.
•	Google created the MediaPipe, a portable hand tracking framework. It recognizes the joints and tips of 21 hand landmarks.
•	Pyttsx3: A Python text-to-speech conversion tool. It translates recognized text into audio and operates offline.
•	Requests Library: Used for sending HTTP POST requests and retrieving image frames from the ESP32-CAM's IP stream.

In order to extract 26 alphabets hand landmarks, this project uses the ESP32-CAM to record hand gestures in real time. The gestures are then processed using MediaPipe and OpenCV. Without training data, static ASL alphabet gestures are recognized using a rule-based logic. The offline pyttsx3 engine is used to turn the recognized letters into words and then into speech. This method is perfect for assistive communication in low-resource environments because it is portable, affordable, and internet-free.
