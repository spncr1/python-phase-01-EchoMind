#pip install openai python-dotenv - keeping as a placeholder in case I need to install again, but currently is installed for project
from openai import OpenAI
from dotenv import load_dotenv
import os
import pygame
import time
import speech_recognition as sr
import whisper
from gtts import gTTS
from playsound import playsound
import tempfile

# LOAD API KEY
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# LOAD WHISPER (STT)
model = whisper.load_model("base")

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
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...") # or Listening...
            print("Recording audio to file...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                with open(temp_audio.name, "wb") as f:
                    f.write(audio.get_wav_data())

            print("Transcribing with Whisper...")
            result = model.transcribe(temp_audio.name)
            query = result["text"].lower()
            print("You said:", query)
            return query.lower()
        except Exception as e:
            speak("Error. There was an issue with the transcription sir.")
            speak(f"{e}")
            return ""

# WAKE WORDS LIST
wake_words = ["wake up",
              "are you awake",
              "are you there",
              "initiate startup",
              "startup sequence"]

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
            wake_word_phrase = recognizer.recognize_google(audio).lower()
            print("Heard:", wake_word_phrase)
            if wake_word_phrase in wake_words:
                print("Playing startup sound...")
                play_sound("/Users/spncr1/Desktop/Coding/Projects/Python Projects/personal-ai-assistant-(name)/phase 1/python-phase-01-EchoMind/startup.mp3")
                speak("EchoMind online. Awaiting your command, sir.")
                return True
        except Exception as e:
            print(f"Error in wake word detection: {e}")
        return False

client = OpenAI()

# ASK GPT FUNCTION
def ask_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # tells OpenAI which of their models we would like to use
            messages = [ # provides context to the model
                {"role":"system", "content":"You are EchoMind, an interactive personal voice assistant."}, # defines who EchoMind is
                {"role":"user", "content": prompt} # defines what my role as a user is
            ],
            max_tokens=100,
            temperature=0.8, # controls randomness/creativity, where closer to 1 is more creative (varied replies), and closer to 0 is more deterministic, focused answers
        ) # needed to send a prompt to a GPT chat model
        answer = response.choices[0].message.content # accesses the model's reply in the new OpenAI Python client, which then returns this text as the assistant's answer
        return answer
    except Exception as e: # for catching any error that may occur during runtime i.e., network issue, bad API key, OpenAI quota exceeded etc.
        print(f"Error in communicating with GPT: {e}") # print the error instead of allowing it to crash our program
        return "Sorry sir, my brain is malfunctioning"

# MAIN LOGIC
def main ():
    query = listen_command()

    if query: # if user asks for something the assistants response will be to implement the logic created in our ask_gpt function - this is communicated via audio using the speak() function
        response = ask_gpt(query)
        speak(response)
    else:
        pass
        #speak("I do not recognize your command. Please try again sir.")

if __name__ == "__main__":
    if wait_for_wake_word():
        main()