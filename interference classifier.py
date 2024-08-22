import time
import pickle
import cv2
import mediapipe as mp
import numpy as np
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import pygame
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Load the model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize MediaPipe hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {i: chr(65 + i) for i in range(26)}

# Variables for storing detected letters and forming words
detected_letters = []
current_word = ""
translator = None  # Translator will be set based on language selection
language_selected = False
selected_language_code = None

# Define the available languages
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Bengali": "bn",
    "Urdu": "ur",
    "Turkish": "tr",
    "Swahili": "sw",
    "Thai": "th",
    "Vietnamese": "vi",
    "Hebrew": "he",
    "Polish": "pl",
    "Czech": "cs",
    "Hungarian": "hu",
    "Romanian": "ro",
    "Danish": "da",
    "Norwegian": "no",
    "Finnish": "fi",
    "Swedish": "sv",
    "Greek": "el",
    "Bulgarian": "bg",
    "Serbo-Croatian": "sr",
    "Malay": "ms",
    "Indonesian": "id",
    "Marathi": "mr"
}

# GUI for language selection
def set_language(language_code):
    global translator, language_selected, selected_language_code
    translator = GoogleTranslator(source='auto', target=language_code)
    language_selected = True
    selected_language_code = language_code
    root.quit()  # Close the GUI

def on_language_change(event):
    language_code = languages[language_combobox.get()]
    set_language(language_code)

def create_gui():
    global language_combobox, root
    root = tk.Tk()
    root.title("Language Selection")
    root.geometry("300x150")

    # Create a dropdown menu for language selection
    language_combobox = ttk.Combobox(root, values=list(languages.keys()))
    language_combobox.bind("<<ComboboxSelected>>", on_language_change)
    language_combobox.pack(pady=20)

    root.mainloop()

def show_language_selection():
    # Start GUI in a separate thread
    gui_thread = Thread(target=create_gui)
    gui_thread.start()
    gui_thread.join()  # Wait for GUI thread to complete

# Updated speak_text function using gTTS and pygame
def speak_text(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        tts.save("temp.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the audio to finish playing
            continue
        pygame.mixer.music.stop()
        pygame.mixer.quit()  # Ensure the mixer is properly closed
        time.sleep(0.5)  # Add a small delay to ensure the file is released
        os.remove("temp.mp3")
    except Exception as e:
        print(f"Error speaking text: {e}")

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]

        # Draw rectangle and put text on frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)

    # Check for key presses
    key = cv2.waitKey(1)

    # Append letter to current word on spacebar press
    if key == ord(' '):  # Spacebar
        detected_letters.append(predicted_character)
        current_word = ''.join(detected_letters)

    # Display the current word on the frame
    cv2.putText(frame, current_word, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3, cv2.LINE_AA)

    # Show language selection GUI and translate the word when Enter is pressed
    if key == 13 or key == 10:  # Enter key
        if current_word:
            # Show the language selection GUI for each word
            show_language_selection()
            if language_selected:
                # Translate the word to the selected language
                translated_word = translator.translate(current_word)
                print("Translated word:", translated_word)

                # Use gTTS to speak the translated word
                speak_text(translated_word, selected_language_code)

                # Reset detected_letters and current_word for the next word
                detected_letters = []
                current_word = ""

    # Exit if 'q' is pressed
    if key == ord('q'):
        break

    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()