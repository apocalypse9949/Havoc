import os
import time
import json
import shutil
import subprocess
import pyautogui
import pyttsx3
import cv2
import numpy as np
import face_recognition
import speech_recognition as sr
import pyaudio
import pvporcupine
import socket
from datetime import datetime


ASSISTANT_NAME = "Neo"  

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except:
        return ""

def authenticate_user():
    speak("Scanning face to unlock assistant")
    video_capture = cv2.VideoCapture(0)
    known_face_encodings = []
    known_face_names = ["User"]  
    user_image = face_recognition.load_image_file("user_face.jpg")  
    known_face_encodings.append(face_recognition.face_encodings(user_image)[0])
    
    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if True in matches:
                speak("Welcome back!")
                video_capture.release()
                cv2.destroyAllWindows()
                return True
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return False

def execute_command(command):
    if "open browser" in command:
        speak("Opening browser")
        os.system("start chrome")
    elif "play music" in command:
        speak("Playing music")
        os.system("start wmplayer")
    elif "move file" in command:
        speak("Which file should I move?")
        file_name = listen_command()
        speak("Where should I move it?")
        destination = listen_command()
        try:
            shutil.move(file_name, destination)
            speak("File moved successfully.")
        except Exception as e:
            speak(f"Error: {str(e)}")
    elif "search file" in command:
        speak("What is the file name?")
        file_name = listen_command()
        for root, dirs, files in os.walk("C:\\"):
            if file_name in files:
                speak(f"Found {file_name} in {root}")
                return
        speak("File not found.")
    elif "what time is it" in command:
        speak("The time is " + datetime.now().strftime("%H:%M"))
    elif "shutdown" in command:
        speak("Shutting down system")
        os.system("shutdown /s /t 1")
    elif "sync devices" in command:
        speak("Synchronizing data across devices.")
        subprocess.run("syncthing")
    else:
        speak("I didn't understand that.")

# === Main Execution ===
if authenticate_user():
    speak(f"Hello! I am {ASSISTANT_NAME}. How can I help you?")
    while True:
        command = listen_command()
        execute_command(command)
        time.sleep(1)
