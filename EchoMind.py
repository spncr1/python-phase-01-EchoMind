#pip install openai python-dotenv
#import openai
#import pyttsx3 # converts text to speech
#engine = pyttsx3.init()
import pygame
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import tempfile
import os

# TEXT-TO-SPEECH HANDLER
def speak (text):
    print(f"EchoMind says: {text}")
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        playsound(fp.name)
        os.remove(fp.name)

# LISTEN FOR COMMAND
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...") # or Listening...
            query = recognizer.recognize_google(audio, language='en-in') # variable that stores user query as speech (specifically understanding it as english)
            print("You said:", query)
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry sir, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("There was a problem connecting to the speech service.")
            return ""

# WAKE WORDS LIST
wake_words = ["are you awake",
              "echomind, you there?",
              "initiate startup",
              "echomind startup sequence"]

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# WAIT FOR WAKE WORD FUNCTION
def wait_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Awaiting wake command...")
        audio = recognizer.listen(source)
        try:
            phrase = recognizer.recognize_google(audio).lower()
            print("Heard:", phrase)
            if phrase in wake_words:
                print("Playing startup sound")
                play_sound("/Users/spncr1/projects/echomind/startup.mp3")
                print("Speaking wake confirmation")
                speak("EchoMind online. Awaiting your command, sir.")
                print("Wake word confirmed")
                return True
        except Exception as e:
            print(f"Error in wake word detection: {e}")
        return False

# MAIN LOGIC
def main ():
    # VOICE STARTUP
    speak("I am EchoMind, your voice assistant, how may I help you sir?")

    query = listen_command()

    if 'current time' in query:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif 'date' in query:
        now = datetime.now()
        current_date = now.strftime("%d/%m/%Y")
        speak(f"The current date is {current_date}")
    else:
        speak("Sir, I'm still learning. Please try asking me to do something simpler.")

if __name__ == "__main__":
    if wait_for_wake_word():
        main()