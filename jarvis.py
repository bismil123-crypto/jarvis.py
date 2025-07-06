import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
from requests import get
import pywhatkit as kit
import smtplib
import sys
import requests
import pygetwindow as gw
import pyautogui  # For alt-tab functionality
import time  # For adding delays
import geocoder
import instaloader
import PyPDF2
import pdfplumber
from langdetect import detect
from deep_translator import GoogleTranslator
from googletrans import Translator
import openai


# Initialize the text-to-speech engine

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
ACCESS_PASSWORD = "123"

def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def authenticate_user():
    """Password-based security authentication."""
    speak("Please say the password to access me.")
    password = takeCommand().lower()
    if ACCESS_PASSWORD in password:
        speak("Access granted. Welcome!")
        return True
    else:
        speak("Access denied. Invalid password.")
        return False
def detect_and_translate():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for translation...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing and translating...")
        query = r.recognize_google(audio)
        print(f"Original spoken text: {query}")
        
        detected_lang = detect(query)
        print(f"Detected language: {detected_lang}")

        if detected_lang != 'en':
            translated_text = GoogleTranslator(source=detected_lang, target='en').translate(query)
            print(f"Translated text: {translated_text}")
            speak(f"Translating from {detected_lang}.")
            speak(translated_text)
        else:
            speak("The text is already in English.")
            speak(query)
    except Exception as e:
        print(f"An error occurred during recognition or translation: {e}")
        speak("I encountered an error while translating.")
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a question...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the service.")
        return None

def language_practice( word, target_language):
       print(f"Practicing {word} in {target_language}")
openai.api_key = ""
#openai.api_key = "your_openai_api_key_here"  # Replace with your OpenAI API key
def ask_question(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or any other model you prefer
        messages=[{"role": "user", "content": question}],
    )
    
    print(response['choices'][0]['message']['content'].strip())

import random

def therapist_mode():
    advice = [
        "Take a deep breath. You’re doing great!",
        "Remember to take breaks and stay hydrated.",
        "Try listing three things you're grateful for today.",
        "If things feel overwhelming, start with one small task."
    ]
    print(random.choice(advice))
import speech_recognition as sr
from googletrans import Translator

translator = Translator()
recognizer = sr.Recognizer()

def translate_conversation():
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
        original_text = recognizer.recognize_google(audio, language="es")
        translation = translator.translate(original_text, dest="en")
        print(f"Original: {original_text}")
        print(f"Translated: {translation.text}")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
        detect_and_translate(query)  # Call translation function
    except Exception as e:
        print("Say that again, please...")
        return "None"
    return query

# Use detect_and_translate to process language recognition and translation


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-pk")
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again, please...")
        return "None"
    return query

def pdf_reader():
    speak("Opening PDF reader")
    
    # Open the PDF file (update the path as needed)
    file_path = r"C:\Users\Sj\Desktop\sample.pdf"  # Replace with your PDF file path
    
    try:
        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            speak(f"The PDF has {total_pages} pages.")
            
            # Ask the user for the page number
            speak("Which page number do you want to hear?")
            page_input = takeCommand().lower()  # Get user input for page number
            print(f"User input: {page_input}")  # For debugging

            # Extract the number from the input string
            try:
                page_number = int(''.join(filter(str.isdigit, page_input)))  # Get digits only
            except ValueError:
                speak("Sorry, I didn't catch a valid page number.")
                return

            # Validate the page number
            if 1 <= page_number <= total_pages:
                page = pdf.pages[page_number - 1]  # Page numbers are 0-indexed
                text = page.extract_text()  # Extract text from the specified page
                
                if text:  # Check if text was extracted
                    speak(f"Reading page {page_number}.")
                    speak(text)  # Read the text using the TTS engine
                else:
                    speak("Sorry, I couldn't extract any text from that page.")
            else:
                speak("Sorry, that page number is out of range.")
    
    except FileNotFoundError:
        speak("Sorry, I could not find the PDF file.")
    except Exception as e:
        speak("An error occurred while reading the PDF.")
        print(f"Error: {e}")

    speak("PDF reader closed.")
def wishme():
    now = datetime.datetime.now()
    hour = int(now.hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Roobie dear aiman. How can I help you?")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("@gmail.com", "")  # Use secure method for password
        server.sendmail("@gmail.com", to, content)
        server.quit()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the email.")

def tell_news():
    url = ''  # Replace with your API key
    main_page = requests.get(url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(min(len(head), len(day))):  # Ensure it doesn't exceed available articles
        speak(f"Today's {day[i]} news is: {head[i]}")

def switch_window():
    try:
        windows = gw.getAllTitles()
        speak("Here are the open windows.")
        for i, window in enumerate(windows, start=1):
            print(f"{i}. {window}")
            speak(f"{i}. {window}")
        speak("Which window would you like to switch to?")
        choice = takeCommand()

        for window in windows:
            if choice.lower() in window.lower():
                gw.getWindowsWithTitle(window)[0].activate()
                speak(f"Switched to {window}")
                return
        speak("I couldn't find that window.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I couldn't switch the window.")
def set_speaking_speed(speed):
    """Set the speaking speed."""
    engine.setProperty('rate', speed)
def adjust_speed():
    speak("Please tell me the speaking speed you prefer. For example, you can say 'slow', 'normal', or 'fast'.")
    speed_command = takeCommand().lower()

    if "slow" in speed_command:
        set_speaking_speed(150)  # Slower speed
        speak("Speaking speed set to slow.")
    elif "normal" in speed_command:
        set_speaking_speed(200)  # Normal speed
        speak("Speaking speed set to normal.")
    elif "fast" in speed_command:
        set_speaking_speed(250)  # Faster speed
        speak("Speaking speed set to fast.")
    else:
        speak("Sorry, I didn't understand the speed setting. Keeping the default speed.")
def main():
    """Main execution flow."""
    if not authenticate_user():
        sys.exit()
    wishme()
    while True:
        query = takeCommand().lower()

        if 'play' in query:
            song_name = query.replace("play", "").strip()
            if song_name:
                speak(f"Playing {song_name} on YouTube.")
                kit.playonyt(song_name)
            else:
                speak("Please specify the name of the song.")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            cn = takeCommand().lower()
            webbrowser.open(f"{cn}")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")

        elif 'open chatgpt' in query:
            webbrowser.open("https://www.chatgpt.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir or Madam, the time is {strTime}.")
        elif 'lang practice' in query:
         speak("Which language do you want to practice?")
         lang = takeCommand().lower()  # Get the language from the user
         word = "how are you"  # Replace this with the word you want to practice (or get from the user)
         target_language = lang  # Set the target language based on the user's input
         language_practice(word, target_language)  # Pass both arguments when calling the function

        elif 'ask question' in query:
         speak("What question do you want to ask?")
         question = listen()  # Assuming you have a function `listen()` to capture user input
         ask_question(question)  # Pass the question to the function

        elif 'translate convo'in query:
            speak("Which language do you want to translate to?")
            translate_conversation()
        elif 'therapy'in query:
            speak("Which type of therapy do you want to do?")
            therapist_mode()
        
        elif 'open code' in query:
            codePath = ""
            os.startfile(codePath)

        elif 'open command' in query:
            os.system('start cmd')

        elif 'open notepad' in query:
            os.system('notepad.exe')

        elif 'open word' in query:
            os.system('winword.exe')

        elif 'ip address' in query:
            ip = get('https://api').text
            speak(f"Your IP address is {ip}")

        elif 'send message' in query:
            speak("Who do you want to send the message to?")
            recipient_number = ""  # Replace with user input for flexibility
            message = "This is a test message from Jarvis."
            
            now = datetime.datetime.now()
            hour = now.hour
            minute = (now.minute + 1) % 60
            try:
                kit.sendwhatmsg(recipient_number, message, hour, minute)
                speak("Message has been scheduled to send in 1 minute.")
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("Sorry, I couldn't send the message.")

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand().lower()
                to = ""  # Replace with actual recipient email
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send the email.")

        elif 'tell the news' in query:
            speak("Please wait while I fetch the news.")
            tell_news()

        elif 'switch window' in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep
            pyautogui.keyUp('alt')# Call the switch_window function


        elif 'where i am'  in query:
            speak("Let me check that for you.")
            g = geocoder.ip('https://api.')  # 'me' uses your current IP address

            if g.ok:
              speak(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")
              speak(f"Address: {g.city}, {g.state}, {g.country}")
              #print(f"Latitude: {g.latlng[0]}, Longitude: {g.latlng[1]}")
              #print(f"Address: {g.city}, {g.state}, {g.country}")
            else:
              #print("Unable to retrieve location")
              speak("Unable to retrieve location")
        elif 'battery updates'in query:
            import psutil
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"Battery is at {percentage}%")
        elif 'shutdown' in query:
            speak("Shutting down the system")
            shutdown = input("Are you sure you want to shut down the system? (yes/no)")
            if shutdown == "yes":
                os.system("shutdown /s /t 1")
            else:
                speak("Shutting down cancelled") 
        elif 'speed of internet'in query:
            
            import speedtest
            st = speedtest.Speedtest()
            dl = st.download() / 1_000_000  # Convert to Mbps
            up = st.upload() / 1_000_000  # Convert to Mbps
            speak(f"Sir, we have {dl:.2f} Mbps downloading speed and {up:.2f} Mbps uploading speed.")
        elif 'translate'in query:
            speak("Please say the text you want to translate")
            detect_and_translate()

        elif 'insta' in query:
            speak("Please say the Instagram username you want to look up.")
            username = takeCommand().lower()
            if username and username != "none":
                webbrowser.open(f"https://www.instagram.com/{username}")
                speak(f"Here is the profile of user: {username}")
                speak("Would you like to download the profile picture?")
                condition = takeCommand().lower()
                if 'yes' in condition:
                    try:
                     mod = instaloader.Instaloader()
                     mod.download_profile(username, profile_pic_only=True)
                     speak("Profile picture is downloaded.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        speak("Sorry, I couldn't download the profile picture.")
                else:
                    speak("Okay, not downloading the profile picture.")
        elif 'take screenshot'in query:
            speak("Tell name for this ss file")
            name=takeCommand().lower()
            speak("hold the screen for second")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save("f{name}.png")
            speak("Screenshot saved")
        elif 'send sms'in query:
            speak("what should i do:")
            msz=takeCommand()
            from twilio.rest import Client
            account_sid = ''
            auth_token = ''
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            
            from_='+1234567890',  # Replace with your Twilio number
            body='Ahoy 👋am testing robbies ai:',
            to='+'  # Replace with the recipient's number
            )
            print(message.sid)
        elif'volume up'in query:
            pyautogui.press("volumeup")
        elif'volume down'in query:
            pyautogui.press("volumedown")
        elif 'mute'in query:
            pyautogui.press("volumemute")
        elif'alarm'in query:
            speak("please tell me the time to set alarm:")
            tt=takeCommand()
            tt=tt.replace("set alarm to"," ")
            tt=tt.replace("at"," ")
            tt=tt.upper()
            import MyAlarm
            MyAlarm.alarm(tt)
        elif 'read pdf'in query:
            pdf_reader()
        elif 'no thanks' in query:
            speak("Okay, have a good day!")
            sys.exit()
if __name__ == "__main__":
    main()
