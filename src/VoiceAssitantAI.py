import speech_recognition as s
import pyttsx3 
import datetime
from queue import Empty
import wikipedia
import webbrowser
import requests
import json
import os
import time
import subprocess
import wolframalpha

texttospeech = pyttsx3.init('sapi5')

texttospeech.setProperty('voice', texttospeech.getProperty('voices')[0].id)

import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

import colorama 
colorama.init()
from colorama import Fore, Style, Back

import random
import pickle

with open("../src/intent.json") as file:
    data = json.load(file)

def speak(text):
    texttospeech.say(text)
    texttospeech.runAndWait()

def takeCommand():
    r=s.Recognizer()
    with s.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

if __name__=='__main__':
      # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20

    hour=datetime.datetime.now().hour
    if hour>0 and hour<12:
        speak("Hello, Good Morning,")
        speak("Tell me how can I help you now?")
        print('Hello, Good Morning')
        print("Tell me how can I help you now?")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        speak("Tell me how can I help you now?")
        print("Hello,Good Afternoon")
        print("Tell me how can I help you now?")
    else:
        speak("Hello,Good Evening")
        speak("Tell me how can I help you now?")
        print("Hello,Good Evening")
        print("Tell me how can I help you now?")

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = takeCommand().lower()
        if inp is None:
             continue
        if "quit" in inp or "good bye" in inp or "ok bye" in inp or "stop" in inp:
            speak('Good bye')
            print('Good bye')
            break

        elif 'time' in inp:
            currentTime=datetime.datetime.now()
            ttime = currentTime.strftime("%c")
            print(f"The time is: {ttime}\n")
            speak(f"the time is {ttime}")

        elif 'search'  in inp:
            url = 'https://www.google.com/search?q='
            inp = inp.replace("search", "")
            webbrowser.open_new(url + inp)

        elif 'wikipedia' in inp:
            speak('Searching Wikipedia...')
            inp =inp.replace("wikipedia", "")
            results = wikipedia.summary(inp, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in inp:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'who are you' in inp or 'what can you do' in inp:
            speak('I am a Simple ChatBot. I am programmed to do small tasks')

        elif "who made you" in inp or "who created you" in inp:
            speak(f"I was built by Ria, Dhruv and Alish")
            print(f"I was built by Ria, Dhruv and Alish")
        elif 'open google' in inp:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in inp:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif 'ask' in inp:
            speak("I can answer omputational and geographical questions")
            question=takeCommand()
            appid = "2WGHR5-HHQ78XU44V"
            client = wolframalpha.Client("2WGHR5-HHQ78XU44V")
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
        
        elif "log off" in inp or "signout" in inp:
            speak("Your PC will log off in 10 seconds, please close all you applications")
            subprocess.call(["shutdown", "/h"])


        
        elif "weather" in inp or "forecast" in inp or "temperature" in inp:
            APIkey="88ee30e21293490d319a4a25ec3672fa"
            url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the name of the city")
            city=takeCommand()
            urlLink=url+"appid="+APIkey+"&q="+city
            answer = requests.get(urlLink)
            weatherToday=answer.json()
            if weatherToday["cod"]!="404":
                today=weatherToday["main"]
                weather = today["temp"]                
                value = weatherToday["weather"]
                weather_description = value[0]["description"]
                speak(f" Temperature in kelvin unit is " +
                      str(weather))
                print(f" Temperature in kelvin unit = " +
                      str(weather))
            else:
                speak(" City Not Found ")
        else:
            result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                truncating='post', maxlen=max_len))
            tag = lbl_encoder.inverse_transform([np.argmax(result)])

            for i in data['intents']:
                if i['tag'] == tag:
                    print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL , np.random.choice(i['responses']))
                    speak( np.random.choice(i['responses']))

        # print(Fore.GREEN + "ChatBot:" + Style.RESET_ALL,random.choice(responses))
    
print(Fore.YELLOW + "Start messaging with the bot (type quit to stop)!" + Style.RESET_ALL)