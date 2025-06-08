import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change to [1] if you prefer female voice
engine.setProperty('rate', 130)
engine.setProperty('volume', 2.0)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak(f"The current time is {current_time}")
    print(f"The current time is {current_time}")

def tell_date():
    now = datetime.datetime.now()
    speak(f"Today's date is {now.day} {now.strftime('%B')} {now.year}")
    print(f"Today's date is {now.day}/{now.month}/{now.year}")

def wish_me():
    speak("Welcome back!")
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        greet = "Good morning"
    elif 12 <= hour < 16:
        greet = "Good afternoon"
    elif 16 <= hour < 24:
        greet = "Good evening"
    else:
        greet = "Good night"
    speak(greet)
    assistant_name = load_name()
    speak(f"{assistant_name} at your service. How can I help you?")
    print(f"{assistant_name} at your service.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Timeout. Try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return None

def take_screenshot():
    img = pyautogui.screenshot()
    path = os.path.expanduser("~/Pictures/screenshot.png")
    img.save(path)
    speak("Screenshot saved.")
    print(f"Screenshot saved at {path}")

def play_music(song_name=None):
    music_dir = os.path.expanduser("~/Music")
    try:
        songs = os.listdir(music_dir)
        if song_name:
            songs = [song for song in songs if song_name.lower() in song.lower()]
        if songs:
            song = random.choice(songs)
            os.system(f"open '{os.path.join(music_dir, song)}'")
            speak(f"Playing {song}")
        else:
            speak("No matching songs found.")
    except Exception as e:
        speak("Unable to play music.")
        print(f"Error: {e}")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)

def set_name():
    speak("What would you like to name me?")
    name = take_command()
    if name:
        with open("assistant_name.txt", "w") as f:
            f.write(name)
        speak(f"I'll be called {name} from now on.")
    else:
        speak("I didn't get that.")

def load_name():
    try:
        with open("assistant_name.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Jarvis"

def search_wikipedia(query):
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything.")

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        if not query:
            continue

        if "time" in query:
            tell_time()

        elif "date" in query:
            tell_date()

        elif "wikipedia" in query:
            search_wikipedia(query.replace("wikipedia", "").strip())

        elif "play music" in query:
            song = query.replace("play music", "").strip()
            play_music(song)

        elif "open youtube" in query:
            speak("Opening YouTube")
            wb.open("https://youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            wb.open("https://google.com")

        elif "open chrome" in query:
            speak("Opening Google Chrome")
            os.system("open -a 'Google Chrome'")

        elif "open safari" in query:
            speak("Opening Safari")
            os.system("open -a Safari")

        elif "open whatsapp" in query:
            speak("Opening WhatsApp")
            os.system("open -a WhatsApp")

        elif "open chatgpt" in query:
            speak("Opening ChatGPT")
            wb.open("https://chat.openai.com")

        elif "change your name" in query:
            set_name()

        elif "screenshot" in query:
            take_screenshot()

        elif "tell me a joke" in query:
            tell_joke()

        elif "open gmail" in query:
            speak("Opening Gmail")
            wb.open("https://mail.google.com")

        elif "open instagram" in query:
            speak("Opening Instagram")
            wb.open("https://instagram.com")

        elif "open facebook" in query:
            speak("Opening Facebook")
            wb.open("https://facebook.com")

        elif "open github" in query:
            speak("Opening GitHub")
            wb.open("https://github.com")

        elif "open stack overflow" in query:
            speak("Opening Stack Overflow")
            wb.open("https://stackoverflow.com")

        elif "open spotify" in query:
            speak("Opening Spotify")
            os.system("open -a Spotify")

        elif "open notes" in query:
            speak("Opening Notes")
            os.system("open -a Notes")

        elif "open vs code" in query or "open visual studio code" in query:
            speak("Opening Visual Studio Code")
            os.system("open -a 'Visual Studio Code'")

        elif "shutdown" in query:
            speak("Sorry, shutting down is not supported on Mac for security.")

        elif "restart" in query:
            speak("Sorry, restarting is not supported on Mac for security.")

        elif "exit" in query or "offline" in query:
            speak("Going offline. Goodbye!")
            break