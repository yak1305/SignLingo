SignLingo

This Python-based graphical user interface (GUI) application utilizes advanced computer vision techniques to detect sign language gestures in real-time. The detected gestures are automatically translated into text, which can then be converted into speech in various languages. The application offers a seamless and intuitive experience for communicating across different languages through sign language and it also bridges communication gaps and enhance accessibility for individuals who use sign language.

-> Features:


1) Real-Time Gesture Detection : Uses OpenCV and MediaPipe to detect and recognize sign language gestures.

 
2) Automatic Text Conversion : Converts recognized gestures into corresponding text without the need for manual input.

 
3) Multi-Language Translation : Supports translation of detected text into multiple languages.

   
4) Text-to-Speech Integration : Converts translated text into speech, allowing for easy communication in the selected language.

 
5) Customizable Language Selection : Users can choose from a variety of languages for translation and speech output.


-> Basic Walkthrough


1) Collecting images in real time : This Python script uses the os and cv2 (OpenCV) libraries to capture and save images from a webcam. It begins by setting up a directory structure to store images for 26 
   different classes. The script then accesses the webcam and displays a prompt on the video feed, instructing the user to press "Q" when ready to start capturing images. Once "Q" is pressed, the script captures 
   100 images for each class, saving them in the appropriate directories. Finally, the webcam is released when all images have been captured.


2) Creating a Dataset : This Python script uses os, pickle, warnings, mediapipe, cv2, and matplotlib.pyplot to process hand images. It reads images, extracts and normalizes hand landmark coordinates using 
   MediaPipe, and saves the data and labels in a data.pickle file for machine learning use


3) Training a Dataset : This Python script uses pickle, sklearn, and numpy to train a Random Forest classifier on hand landmark data, evaluate its accuracy, and save the model to a file.


4) Gesture Recognition and converting it into other languages : This Python script captures video from a webcam, detects hand landmarks using MediaPipe, and predicts hand signs using a pre-trained Random Forest 
   model. It displays the detected sign on the video feed and translates the recognized word into a selected language using Google Translator. The translated text is then spoken using gTTS and pygame. The script 
   includes a GUI for language selection and processes video frames in real-time until the user exits by pressing 'q'.














