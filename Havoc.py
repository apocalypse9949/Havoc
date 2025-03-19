import speech_recognition as sr
import pyttsx3
import pyautogui
import os
import time
import webbrowser
from pocketsphinx import LiveSpeech

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command if command.strip() else None
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
            return None

def open_application(app_name):
    if "notepad" in app_name:
        os.system("notepad")
    elif "chrome" in app_name:
        os.system("start chrome")
    elif "explorer" in app_name:
        os.system("explorer")
    elif "spotify" in app_name:
        os.system("start spotify:")
    else:
        speak("Application not recognized.")

def open_youtube_in_brave():
    brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    url = "https://www.youtube.com"
    if os.path.exists(brave_path):
        webbrowser.register("brave", None, webbrowser.BackgroundBrowser(brave_path))
        webbrowser.get("brave").open(url)
    else:
        print("Brave browser not found. Please check the installation path.")

def control_pc(command):
    if "shutdown" in command:
        speak("Shutting down...")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting...")
        os.system("shutdown /r /t 1")
    elif "sleep" in command:
        speak("Putting PC to sleep...")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def write_note():
    speak("What should I write?")
    note = listen()
    if note:
        with open("note.txt", "a") as f:
            f.write(note + "\n")
        speak("Note saved.")

def online_search(query):
    speak(f"Searching for {query} online.")
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)

def play_song_in_spotify(song_name):
    if not song_name:
        speak("I didn't catch the song name. Try again.")
        return
    open_application("spotify")
    time.sleep(8) 
    pyautogui.hotkey('ctrl', 'l')  
    time.sleep(2)
    pyautogui.write(song_name)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.press('tab', presses=3, interval=1)  
    time.sleep(1)
    pyautogui.press('enter')
    speak(f"Playing {song_name} on Spotify.")

def wake_word_detection():
    speak("Listening for wake word...")
    speech = LiveSpeech(lm=False, keyphrase='arise', kws_threshold=1e-20)
    for phrase in speech:
        print("Wake word detected!")
        speak("Assistant Activated.")
        assistant()
        break

def assistant():
    speak("Assistant ready. Say your command.")
    while True:
        command = listen()
        if command is None:
            continue  

        command = command.strip()

        if "open" in command:
            app = command.replace("open", "").strip()
            open_application(app)
        elif "play" in command:
            song = command.replace("play", "").strip()
            play_song_in_spotify(song)
        elif "shutdown" in command or "restart" in command or "sleep" in command:
            control_pc(command)
        elif "write a note" in command:
            write_note()
        elif "search for" in command:
            query = command.replace("search for", "").strip()
            online_search(query)
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I did not understand. Try again.")

if __name__ == "__main__":
    wake_word_detection()
