from dotenv import load_dotenv
load_dotenv()
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
import google.generativeai as genai
from gtts import gTTS # note: even pyttsx3 or elevenlabs can be used, but gTTS is more natural
import pygame

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv('NEWS_API_KEY')

# info: speak function using pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# info: another speak function using gTTS
# def speak(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')
#     pygame.mixer.init()
#     pygame.mixer.music.load('temp.mp3')
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

#     pygame.mixer.music.stop()
#     pygame.mixer.music.unload()

#     os.remove('temp.mp3')

def aiProcess(command):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="You are a virtual assistant named Jarvis skilled in general tasks like Alexa, Siri, and Google Assistant. You should always respond in the persona of Jarvis. Give short and precise responses.",
    )

    completion = model.generate_content(command)
    return completion.text

def list_microphones():
    """List available microphones for debugging"""
    print("Available microphones:")
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {i}: {microphone_name}")
    return sr.Microphone.list_microphone_names()

def processCommand(c):
    if 'open google' in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif 'open youtube' in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif 'open instagram' in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif 'open twitter' in c.lower():
        speak("Opening Twitter")
        webbrowser.open("https://www.x.com")
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif 'open chatgpt' in c.lower():
        speak("Opening ChatGPT")
        webbrowser.open("https://www.chatgpt.com")
    elif 'what is your name' in c.lower():
        speak("I am Jarvis, your personal assistant.")

# Music play command
    elif c.lower().startswith('play'):
        song = c.lower().split(" ")[1] # info: Get the song name after 'play/0' from the list that split will create [play, song_name]
        link = musicLibrary.music[song]
        webbrowser.open(link)

# News fetching command
    elif 'news' in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            # Extract the articles
            articles = data.get('articles', [])
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # let openai handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    # List available microphones for debugging
    list_microphones()
    
    # Test microphone availability
    print("Testing microphone...")
    try:
        with sr.Microphone() as source:
            print("Microphone found and working")
    except Exception as e:
        print(f"Microphone error: {e}")
        exit(1)
    
    # Listen for the wake word "Jarvis"
    print("Say 'Jarvis' to activate...")
    
    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        r.energy_threshold = 4000  # Adjust based on your environment
        r.dynamic_energy_threshold = True

        # recognize speech using google
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=1.0)
                print("Listening for wake word 'Jarvis'...")
                audio = r.listen(source, timeout=10, phrase_time_limit=3)
            word = r.recognize_google(audio)
            print(f"You said: {word}")
            if word.lower() == 'jarvis':  # Fixed: comparing lowercase to lowercase
                speak('Yes, I am listening')
                # Listen for the next command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=10, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("No speech detected, continuing to listen...")
        except sr.UnknownValueError:
            print("Could not understand audio, continuing to listen...")
        except sr.RequestError as e:
            print(f"Google Speech Recognition service error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
