from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os
from dotenv import load_dotenv
import pygame
import time
import speech_recognition as sr
import whisper
#from gtts import gTTS
from playsound import playsound
import tempfile
#import requests

# LOAD API KEY
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# ELEVENLABS TTS SETTINGS
ELEVENLABS_VOICE_ID = "PYVunL4QLJz0auimQhZB" # Set to "Aussie JARVIS" for now

# LOAD WHISPER (STT)
model = whisper.load_model("base")

# INITIATE ELEVENLABS CLIENT ONCE WITH API KEY
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# TEXT-TO-SPEECH HANDLER
def speak (text, voice_id = ELEVENLABS_VOICE_ID):
    print(f"EchoMind says: {text}") # currently a slight delay in the delivery of this text (takes a few seconds to speak output, yet the text it is about to speak is already printed to the console window)

    try:
        # Use ElevenLabs client to generate audio (UPDATED)
        audio = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",  # Optional: specify model if desired
            output_format="mp3_44100_128"
        )

        # Play audio using ElevenLabs helper play() (NEW)
        play(audio)

        # ALTERNATIVE AUDIO PLAYBACK OPTION IN CASE THE ABOVE FAILS
        #with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
             #fp.write(audio)
             #temp_audio_path = fp.name
        #pygame.mixer.init()
        #pygame.mixer.music.load(temp_audio_path)
        #pygame.mixer.music.play()
        #while pygame.mixer.music.get_busy():
             #time.sleep(0.1)
        #os.remove(temp_audio_path)

    except Exception as e:
        print(f"Error in ElevenLabs TTS: {e}")

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
              "startup sequence",
              "start up",
              "initiate",
              "initialise",
              "turn on"]

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
                play_sound("/Users/spncr1/Desktop/Coding/Projects/Python Projects/personal-ai-assistant-(name)/phase 1/python-phase-01-EchoMind/startup.mp3")
                speak("EchoMind online. Awaiting your command sir.")
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
        speak("I do not recognize your command. Please try again sir.")

if __name__ == "__main__":
    if wait_for_wake_word():
        main()