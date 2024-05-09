import sys

import pyttsx3
import speech_recognition as sr
import datetime
import os
import subprocess
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# speach to text
def take_command():
    r = sr.Recognizer()
    r.pause_threshold = 1
    with sr.Microphone() as source:
        print("Listening ...")
        audio = r.listen(source, timeout=1, phrase_time_limit=5)
    try:
        print("Recognizing ...")

        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}")

    except Exception as e:
        speak("say that again please...")
        return "none"
    return query


def wish():
    hour = int(datetime.datetime.now().hour)
    print(hour)

    if hour >= 0 and hour <= 12:
        speak("Good Morning sir")
    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon sir")
    else:
        speak("Good evening sir ")
    speak("I am your assistant please tell me How may i assist you?")


def getpath(text):
    # file_path = f"{text}.exe"
    # absolute_path = os.path.abspath(file_path)
    command = f"where {text}"
    absolute_path = subprocess.check_output(command, shell=True, universal_newlines=True)
    return absolute_path


def dynamic_file_get():
    pass
    # result = query.split("open", 1)
    # if len(result) > 1:
    #     output = result[1].strip()  # Remove any leading/trailing spaces
    #     b = getPath(output)
    #     n = b.partition('\n')[0]
    #     os.startfile(n)
    # else:
    #     print("Query does not contain a valid filename.")


def send_email(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('dawoodahmed6497@gmail.com','198924aA.')
    server.sendmail('dawoodahmed6497@gmail.com',to,content)
    server.close()


if __name__ == '__main__':
    # speak('hi david, I will be assisting you for your daily tasks projects and other automation')
    # take_command()
    wish()
    while True:
        query = take_command().lower()
        if "open notepad" in query:
            b = getpath("notepad")
            n = b.partition('\n')[0]
            os.startfile(n)
        elif "open command line" in query:
            os.system("start cmd")
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret,img = cap.read()
                cv2.imshow('webcam',img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
        elif "play music" in query:
            music_dir = "D:\\music"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir,rd))
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"sir your ip address is {ip}")
        elif "wikipedia" in query:
            speak("searching wikipedia.....")
            query = query.replace("wikipedia","")
            print(query)
            results = wikipedia.summary(query,sentences = 3)
            speak("according to wikipedia")
            speak(results)
            print(results)
        elif "open youtube" in query:
            webbrowser.open("youtube.com")
        elif "open google" in query:
            speak("sir what should i search on google")
            cd = take_command().lower()
            webbrowser.open(f"{cd}")
        elif "send message" in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")

            # Extract hour and minute
            hour, minute = current_time.split(":")
            hour = int(hour)
            minute = int(minute)

            # Send the message
            kit.sendwhatmsg("+923075984681", "this is texting protocol", 5, 29)
        elif "play songs on youtube" in query:
            kit.playonyt("treat you better")
        elif "send email to david" in query:
            try:
                speak("what should i say")
                content = take_command().lower()
                to = "dawoodahmed6497@gmail.com"
                send_email(to,content)
                speak("email has been sent")
            except Exception as e:
                print(e)
                speak("sorry sir, i am not able to send the email")
        elif "no thanks" in query:
            speak("have a nice day sir")
            sys.exit()
        speak("do you need me to do anything else for you")

