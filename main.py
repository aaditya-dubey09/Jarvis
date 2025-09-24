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

#     os.remove('temp.mp3')

def aiProcess(command):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="You are a virtual assistant named Jarvis skilled in general tasks like Alexa, Siri, and Google Assistant. You should always respond in the persona of Jarvis. Give short and precise responses.",
    )

    completion = model.generate_content(command)
    return completion.text

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
    # Listen for the wake word "Jarvis"

    while True:
        # obtain audio from the microphone
        r = sr.Recognizer()

        # recognize speech using google
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == 'Jarvis':
                speak('Ya')
                # Listen for the next command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
