import os
import time
import json
import subprocess
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyttsx3
import pvporcupine
import pyaudio

# Load Porcupine for Wake Word Detection
WAKE_WORD = "jarvis"  # Customizable
porcupine = pvporcupine.create(keywords=[WAKE_WORD])

# Initialize TTS
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load Speech Recognition Model
model = Model("vosk-model-small-en-us-0.15")
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_command():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_vosk(audio)
        return json.loads(command).get("text", "")
    except:
        return ""

def execute_command(command):
    if "reminder" in command:
        speak("What should I remind you about?")
        reminder_text = listen_command()
        speak(f"Reminder set for {reminder_text}")
        with open("reminders.txt", "a") as file:
            file.write(reminder_text + "\n")
    elif "note" in command:
        speak("What should I write down?")
        note_text = listen_command()
        with open("notes.txt", "a") as file:
            file.write(note_text + "\n")
        speak("Note saved.")
    elif "play music" in command:
        speak("Playing music")
        os.system("start wmplayer")  # Windows Media Player
    elif "send message" in command:
        speak("To whom?")
        contact = listen_command()
        speak("What should I say?")
        message = listen_command()
        subprocess.run(["notepad", "message.txt"])  # Placeholder for actual messaging
        speak(f"Message sent to {contact}.")
    else:
        speak("I didn't understand that.")

# Main Loop for Wake Word Detection
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)
print("Listening for wake word...")

while True:
    pcm = stream.read(512, exception_on_overflow=False)
    if porcupine.process(pcm) >= 0:
        speak("Yes?")
        command = listen_command()
        execute_command(command)
    time.sleep(0.1)
