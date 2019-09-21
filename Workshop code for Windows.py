# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:35:04 2019

@author: Rishabh
"""

from win10toast import ToastNotifier
import time
import os.path  
import sys
import json

import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')       
engine.setProperty('voice', voices[0].id) #use [0] for male and [1] for female

r = sr.Recognizer()

toaster = ToastNotifier()
search = []

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'Replace this with Google Dialog flow token'
#toast = ToastNotifier()

def chatbot(message):  #this function calls the dialogflow api to get a response to your question
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    request.query = message

    response = request.getresponse()
    
    #reader = codecs.getdecoder("utf-8")
    obj = json.load(response)
    try:
        # Get reply from the list
        reply = obj['result']['fulfillment']['speech']
        return reply
    except Exception:
        print("result error")

def texttospeech(alpha): #this is a function for the speech synthesizer
  engine.say(alpha)
  engine.runAndWait()  
  
def listen(): #call this function whenever you want to convert speech to text
   with sr.Microphone() as source:
        print("listening")
        audio = r.listen(source)
    
   try:
        print("analyzing")
        word = r.recognize_google(audio)
        print(word)
        return word
   except Exception:
        print("something went wrong") 

while (3>2): #basically is a loop
    
    word = listen()
    
    try:
        
        search = word.split("Name your bot here!!!!")
        print (search)
    except Exception:
           
        print("empty string")
    
    
    if  len(search) > 1:
        print("Your bot will say this when it hears the key word")
        toaster.show_toast("Grumpy", "I am listening!!!") #push notification syntax is heading followed by body
        texttospeech("I am listening") #this is what your bot says when he starts listening
        question = listen()
        reply = chatbot(question)
        texttospeech(reply)
        print(reply)
        word = ""
    else:
        print("random speech")
    
