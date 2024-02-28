import speech_recognition as sr
import os
import pyttsx3
import webbrowser as web
import datetime
import wikipedia
import pywhatkit
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import requests

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour=datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!,Sir")
    speak("I am JARVIS, Sir. Please tell me what to do for you?")

def take_command():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        speak("Hmm")
        r.pause_threshold=1
        audio = r.listen(source)

    try:
        print("recognizing.....")
        query = r.recognize_google(audio, language="en-in")
        print(f"User Said: {query}")
        return query
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def open_website(url):
    speak(f"Opening {url} Sir!")
    web.open(url)

def my_location():
    speak("Checking....")
    ip_add = requests.get("https://api.ipify.org").text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    city = geo_d['city']
    state = geo_d['region']
    timezone = geo_d['timezone']
    country = geo_d['country']
    op = "https://www.google.com/maps/place/" + city
    web.open(op)
    print(f"Sir, You are now in {city, state, country} and your time zone is {timezone}.")
    speak(f"Sir, You are now in {city, state, country} and your time zone is {timezone}.")

def google_maps(place):
    url_place = "https://www.google.com/maps/place/" + str(place)
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    target_latlon = location.latitude, location.longitude
    web.open(url=url_place)
    location = location.raw['address']
    target = {'city': location.get('city', ''), 'state': location.get('state', ''), 'country': location.get('country', '')}
    current_loca = geocoder.ip('me')
    current_latlon = current_loca.latlng
    distance = str(great_circle(current_latlon, target_latlon))
    distance = str(distance.split('', 1)[0])
    distance = str(round(float(distance), 2))
    speak(target)
    speak(f"Sir, {place} is {distance} kilometers away from your location")

def main():
    speak("Initializing Jarvis")
    speak("Now I am online")
    speak("Hello, I am Jarvis")
    wish_me()
    while True:
        print("Listening......")
        query = take_command().lower()
        if "open youtube" in query:
            open_website("https://www.youtube.com")
        elif "open google" in query:
            open_website("https://www.google.com")
        elif "open instagram" in query:
            open_website("https://www.instagram.com")
        elif "time" in query:
            current_time=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {current_time}")
        elif "wikipedia" in query:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif "search in youtube for " in query:
            query = query.replace("search in youtube for ", "")
            speak("Searching Youtube for " + query)
            pywhatkit.playonyt(query)
            speak("I hope you find the content you are expecting, Sir")
        elif "open in brave" in query:
            query = query.replace("open in brave", "")
            query = query.replace("Jarvis", "")
            speak("Searching for " + query)
            open_website("https://www." + query)
        elif 'my location' in query:
            my_location()
        elif 'where is' in query:
            place = query.replace("where is ", "")
            place = place.replace("jarvis", "")
            google_maps(place)
        elif 'move up' in query:
            speak("Moving Up, Sir")
        elif 'move down' in query:
            speak("Moving down page, Sir")
        elif "exit" in query:
            speak("Goodbye, Sir")
            exit()

if __name__ == "__main__":
    main()
