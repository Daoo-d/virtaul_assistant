import sys
import pyautogui
import pyttsx3
import speech_recognition as sr
import datetime
import os
import subprocess
import requests
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import pyjokes
import instaloader
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# speach to text
def take_command():
    r = sr.Recognizer()
    r.pause_threshold = 1
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening ...")
                r.adjust_for_ambient_noise(source,duration=0.2)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                print("Recognizing ...")

                query = r.recognize_google(audio,language='en-in')
                print(f"User said: {query}")
                return query

        except Exception as e:
            speak("say that again please...")
        
        
    


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

def news():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=994060ecf9d2440a89e7e72fbb543c52"
    response = requests.get(url).json()
    articles = response["articles"]
    head = []
    days = ["first","second","third"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(days)):
        speak(f"todays {days[i]} news is: {head[i]}")    


def send_email(to,content):
    email = "dawoodahmed6497@gmail.com"
    password = "198924Aa."

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,to,content)
    server.quit()
    speak("email has been sent")


if __name__ == '__main__':
    # speak('hi david, I will be assisting you for your daily tasks projects and other automation')
    # take_command()
    wish()
    while True:
        query = take_command().lower()

        if "youtube" in query:
            speak("sir what should i search on youtube")
            cd = take_command().lower()
            kit.playonyt(f"{cd}")  

        elif "google" in query:
            speak("sir what should i search on google")
            cd = take_command().lower()
            webbrowser.open(f"{cd}")    
            
        elif "open" in query:
            query = query.replace("open","").strip()
            query = query.replace("for","").strip()
            query = query.replace("me","").strip()
            query = query.replace("please","").strip()
            pyautogui.press("super")
            pyautogui.sleep(2)
            pyautogui.typewrite(query)
            pyautogui.sleep(1)
            pyautogui.press("enter")

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

        elif "send email to david" in query:
            try:
                speak("what should i say")
                content = take_command().lower()
                to = "dawoodahmed6497@gmail.com"
                send_email(to,content)
            except Exception as e:
                print(e)
                speak("sorry sir, i am not able to send the email")   

        elif "send message" in query:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")

            # Extract hour and minute
            hour, minute = current_time.split(":")
            hour = int(hour)
            minute = int(minute)

            # Send the message
            kit.sendwhatmsg("+923075984681", "this is texting protocol", 5, 29)

        elif "shut down the system" in query:
            os.system("shutdown /s /t S")

        elif "restart the system" in query:
            os.system("shutdown /r /t S")

        elif "sleep the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")            

        elif "tell me the news"in query:
            speak("searching the latest news...")
            news() 

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.sleep(1)
            pyautogui.keyUp("alt")    

        elif "current location" in query or "where i am" in query or "where we are" in query:
            speak("wait sir,let me check")
            try:
                ip_address = get('https://api.ipify.org').text
                url = (f'https://ipapi.co/{ip_address}/json/')
                response = requests.get(url).json()
                location = {
                    "city":response.get("city"),
                    "region":response.get("region"),
                    "country":response.get("country")
                }
                speak(f"It shows that we are in city : {location['city']}, region : {location['region']} in the country : {location['country']}")
            except:
                speak("sorry sir, due to network issue i am not able to find where we are") 
                pass   

        elif "instagram profile" in query or "profile on instagram" in query:
            speak("sir please enter the username correctly")
            name= input("enter username here")
            webbrowser.open(f"www.instagram.com/{name}")
            speak(f"sir here ids the instagram  profile of the user {name}")
            time.sleep(5)
            speak("sir would you like me to download profile pictue of this account")
            command = take_command().lower()
            if "yes" in command:
                mod = instaloader.instaloader()
                mod.download_profile(name,profile_pic_only = True)
                speak("The image is successfully installed in our main folder.")
            else:
                pass    

        elif "screenshot" in query:
            speak("sir do you want me to take a screenshot of the current window")
            comment = take_command().lower()
            if "yes" in comment:
                speak("Sir please tell me the name for the screenshot to save")
                filename = take_command().lower()
                img = pyautogui.screenshot()
                img.save(f"{filename}.png")
                speak("Sir the screenshot is successfully saved")
            else:
                pass    

        elif "no thanks" in query:
            speak("have a nice day sir")
            sys.exit()
        else:
            speak("i am not able to search this")    
        speak("do you need me to do anything else for you")


            # b = getpath("notepad")
            # n = b.partition('\n')[0]
            # os.startfile(n)
        # elif "open camera" in query:
        #     cap = cv2.VideoCapture(0)
        #     while True:
        #         ret,img = cap.read()
        #         cv2.imshow('webcam',img)
        #         k = cv2.waitKey(50)
        #         if k == 27:
        #             break
        #     cap.release()
        #     cv2.destroyAllWindows()
        
        
        
        # elif "open youtube" in query:
        #     webbrowser.open("youtube.com")
        
        
        
        
