import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLib
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv  
recogniser= sr.Recognizer()
engine= pyttsx3.init()
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
newsAPI = os.getenv("NEWS_API_KEY")

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running to allow the music to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.play()
    os.remove("temp.mp3")


def aiprocess(command):
    client = OpenAI( api_key=api_key,)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant, skilled in general task like alexa and google cloud in very short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open intagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link= MusicLib.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsAPI}")
        if r.status_code==200:
            data=r.json()
            articles=data.get('articles',[])

        for article in articles:
            speak(article['title'])

    else:
        # let openai handle the request
        output=aiprocess(command)
        speak(output)


if __name__=="__main__":
     speak("initializng Jarvis .....")
    #listen for wake word HLO
     while True:
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout= 2, phrase_time_limit=1)
            word= r.recognize_google(audio)
            if(word.lower()=="hello"):
                speak("Yaa")
                #listen for command
                with sr.Microphone() as source:
                    print("jarvis active...")
                    audio = r.listen(source,timeout= 2, phrase_time_limit=1)
                    command= r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("error; {0}".format(e))