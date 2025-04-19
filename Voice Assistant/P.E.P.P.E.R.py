import speech_recognition
import pyttsx3
import os
import webbrowser
import openai
import wikipedia
import pywhatkit as wk
import datetime
import pyautogui
import time
import random
import math
import requests
import urllib.parse
import cv2
from Emotion_model import predict_emotion
from record_voice import record_audio
from bs4 import BeautifulSoup
from llama_cpp import Llama

recognizer =speech_recognition.Recognizer()

#Test to Speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

llm = Llama(model_path="models/llama-2-7b-chat.ggmlv3.q4_0.bin")

def say(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = (datetime.datetime.now().hour)
    if hour >= 4 and hour <= 12:
        say("Good Morning")
    elif hour >= 12 and hour <= 18:
        say("Good Afternoon")
    elif hour >= 18 and hour <= 21:
        say("Good Evening")
    else:
        say("Good Night")

    say("Ready to Comply. What can I do for you ?")

# Conversation memory
chat_history = ""

def chat_with_llama(query):
    global chat_history
    prompt = f"{chat_history}User: {query}\nAI:"

    response = llm(
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
        top_p=0.95,
        repeat_penalty=1.1,
        stop=["User:", "AI"]
    )
    answer = response["choice"][0]["text"].strip()
    chat_history += f"User: {query}\nAI: {answer}\n"
    return answer

def detect_emotion():
    say("Please Speak for sometime so that I can analyse and understand your emotion..")
    record_audio("emotional_sample.wav")
    emotion = predict_emotion("emotional_sample.wav")
    say("Based on your voice, I think you're feeling {emotion}")
    print("Based on your voice, I think you're feeling {emotion}")


CANVAS_START = (400, 300)


def draw_shape_in_paint(shape="line"):
    # Open Microsoft Paint
    os.startfile("C:\\Windows\\System32\\mspaint.exe")
    say(f"Opening Paint and drawing a {shape}")
    
    pyautogui.sleep(2)  # Wait for Paint to open

    # Function to draw a line
    def draw_line():
        pyautogui.moveTo(CANVAS_START[0], CANVAS_START[1], duration=1)
        pyautogui.mouseDown()
        pyautogui.dragRel(400, 0, duration=1)  # Horizontal line
        pyautogui.mouseUp()

    # Function to draw a rectangle
    def draw_rectangle():
        pyautogui.moveTo(CANVAS_START[0], CANVAS_START[1], duration=1)
        pyautogui.mouseDown()
        pyautogui.dragRel(200, 0, duration=0.5)
        pyautogui.dragRel(0, 100, duration=0.5)
        pyautogui.dragRel(-200, 0, duration=0.5)
        pyautogui.dragRel(0, -100, duration=0.5)
        pyautogui.mouseUp()

    # Function to draw a square
    def draw_square():
        pyautogui.moveTo(CANVAS_START[0], CANVAS_START[1], duration=1)
        pyautogui.mouseDown()
        pyautogui.dragRel(100, 0, duration=0.5)
        pyautogui.dragRel(0, 100, duration=0.5)
        pyautogui.dragRel(-100, 0, duration=0.5)
        pyautogui.dragRel(0, -100, duration=0.5)
        pyautogui.mouseUp()

    # Function to draw a triangle
    def draw_triangle():
        pyautogui.moveTo(CANVAS_START[0], CANVAS_START[1], duration=1)
        pyautogui.mouseDown()
        pyautogui.moveRel(100, 0, duration=0.3)
        pyautogui.moveRel(-50, -86, duration=0.3)
        pyautogui.moveRel(-50, 86, duration=0.3)
        pyautogui.mouseUp()

    # Function to draw a circle
    def draw_circle():
        radius = 50
        center_x, center_y = CANVAS_START
        pyautogui.moveTo(center_x + radius, center_y)
        pyautogui.mouseDown()
        for angle in range(0, 360, 10):
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            pyautogui.moveTo(center_x + x, center_y + y, duration=0.02)
        pyautogui.mouseUp()

    # Function to fill color
    def fill_color():
        pyautogui.moveTo(300, 70)  # Bucket tool
        pyautogui.click()
        pyautogui.moveTo(CANVAS_START[0], CANVAS_START[1])
        pyautogui.click()

    if shape == "line":
        draw_line()
    elif shape == "rectangle":
        draw_rectangle()
    elif shape == "square":
        draw_square()
    elif shape == "triangle":
        draw_triangle()
    elif shape == "circle":
        draw_circle()
    elif shape == "fill color":
        fill_color()
    else:
        say("I can't draw that shape. Please choose from line, rectangle, square, triangle, circle, freehand, or use tools like text, eraser, brush, or fill color.")

current_language = "en-in"

def SpeechRecognition():
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(mic)
        try:
            query = recognizer.recognize_google(audio, language = current_language)
            print(f"User Said: {query}")
            return query                    # for the ai to repeat what you just said
        except Exception as e:
            print("Sorry, I couldn't understand that. Please try again.")
            return None

def change_language(new_language):
    global current_language
    supported_language = {
        "en-in": "English (India)",
        "en-us": "English (US)",
        "as": "Assamese",
        "bn": "Bengali",
        "bo": "Bodo",
        "doi": "Dogri",
        "gu": "Gujarati",
        "hi": "Hindi",
        "kn": "Kannada",
        "ks": "Kashmiri",
        "kok": "Konkani",
        "mai": "Maithili",
        "ml": "Malayalam",
        "mni": "Manipuri",
        "mr": "Marathi",
        "ne": "Nepali",
        "or": "Odia",
        "pa": "Punjabi",
        "sa": "Sanskrit",
        "sat": "Santali",
        "sd": "Sindhi",
        "ta": "Tamil",
        "te": "Telugu",
        "ur": "Urdu",
        "ne": "Nepali",
        "si": "Sinhala",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh": "chinese",
        "ja": "Japanese"
    }

    if new_language in supported_language:  # Add more languages as needed
        current_language = new_language
        say(f"Language changed to {new_language}")
        print(f"Language changed to {new_language}")
    else:
        say("Sorry, I don't support that language yet.")
        print("Unsupported language")

def listen_for_wake_word(wake_word = "Mrs. Ports"):
    with speech_recognition.Microphone() as mic:
        print("Listening for Wake Word...")
        while True:
            recognizer.adjust_for_ambient_noise(mic, duration = 0.2)
            audio = recognizer.listen(mic)
            try:
                query = recognizer.recognize_google(audio)
                print(f"User Said: {query}")
                if wake_word in query:
                    print(f"Wake word '{wake_word}' detected!")
                    return True
            except Exception as e:
                pass

def handle_typing(text):
    if 'type' in text.lower(): 
        typed_text = text.lower().replace("type", "").strip()
        if typed_text:
            pyautogui.typewrite(typed_text, 0.1)
        else:
            say("Please tell me what to type.")

def open_camera(save_folder="C:\Users\LENOVO\Pictures\Captured_Images"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        say("Sorry, I can't access the camera.")
        return

    say("Opening the camera. Press S to save a photo or Q to quit.")

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        cv2.imshow('Camera - Press S to save, Q to quit', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
            filepath = os.path.join(save_folder, filename)
            cv2.imwrite(filepath, frame)
            say("Photo captured and saved.")
            print(f"Saved to {filepath}")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def search_google_maps(place):
    searched_url = f"https://www.google.com/maps/search/{place}"
    webbrowser.open(searched_url) 

def google_search_and_read(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to extract featured snippet or the first paragraph
        answer = soup.find('div', class_='BNeawe').text
        if answer:
            say(f"According to Google, {answer}")
            print(f"Google Result: {answer}")
        else:
            say("Sorry, I couldn't find a spoken result. Opening Google.")
            webbrowser.open(url)
    except Exception as e:
        print("Error fetching Google result:", e)
        say("Sorry, I had trouble fetching the search result.")

def take_screenshot():
    try:
        now = datetime.now().strftime("%Y-%m-%D__%H : %M : %S")
        filename = f"screenshot{now}.jpg"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        say(f"Screenshot take and saved as {filename}")
        print(f"Screenshot Saved : {filename}")

    except Exception as e:
        print("Error occured can't take the Screenshot")

sites = [
            ["youtube", "https://youtube.com"],
            ["wikipedia", "https://wikipedia.com"],
            ["facebook", "https://facebook.com"],
            ["springboard", "https://infyspringboard.onwingspan.com"],
            ["linkedin", "https://linkedin.com"],
            ["stack overflow", "https://stackoverflow.com"],
            ["gmail", "https://mail.google.com"],
            ["google", "https://google.com"]
        ]

def open_website(query):
    query = query.lower().strip
    for name, link in sites:
        if name in query:
            webbrowser.open(link)
            return
    
    search_query = urllib.parse.quote_plus(query)
    google_search_url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(google_search_url)

def control_volume(action, times = 15):
    for _ in range(times):
        pyautogui.press(action)

def control_brightness(action, times = 10):
    for _ in range(times):
        pyautogui.press(action)

def write_and_save_in_notepad(text_to_write, filename = "my_note.txt"):
    pyautogui.typewrite(text_to_write, interval= 0.05)

    pyautogui.hotkey('ctrl','S')
    time.sleep(1)

    pyautogui.typewrite(filename)
    pyautogui.press('enter')

def play_music_from_folder():
    folder_path = "C:\Users\LENOVO\music"
    supported_formats = ('.mp3', '.mp4', '.wav')

    songs = [file for file in os.listdir(folder_path) if file.endswith(supported_formats)]

    if not songs:
        say("No music files found in your music folder.")
        return
    
    songs_names = [os.path.splitext(song)[0].lower() for song in songs]

    say("which song would you like to play?")
    print("Available Songs:")
    for i,song in enumerate(songs_names, 1):
        print(f"{i}.{song}")

    user_request = SpeechRecognition().lower()
    print(f"You Said: {user_request}")

    matched_songs = None
    for song,full_filename in zip(songs_names, songs):
        if user_request in song:
            matched_songs = full_filename
            break

    if matched_songs:
        song_path = os.path.join(folder_path, matched_songs)
        print(f"playing: {matched_songs}")
        say(f"Playing {matched_songs}")
        os.startfile(song_path)
    else:
        say("No music files found in your OneDrive Music folder.")

def play_video_from_folder():
    folder_path = "C:\Users\LENOVO\Videos"
    supported_formats = ('.mp4', '.mkv')

    videos = [file for file in os.listdir(folder_path) if file.endswith(supported_formats)]

    if not videos:
        say("No video files found in your music folder.")
        return
    
    video_names = [os.path.splitext(video)[0].lower() for video in videos]

    say("which song would you like to play?")
    print("Available Songs:")
    for i,video in enumerate(video_names, 1):
        print(f"{i}.{video}")

    user_request = SpeechRecognition().lower()
    print(f"You Said: {user_request}")

    matched_video = None
    for video,full_filename in zip(video_names, videos):
        if user_request in song:
            matched_video = full_filename
            break

    if matched_video:
        video_path = os.path.join(folder_path, matched_video)
        print(f"playing: {matched_video}")
        say(f"Playing {matched_video}")
        os.startfile(video_path)
    else:
        say("No music files found in your OneDrive Music folder.")


def open_file_folder_from_PC():
    say("Which file or folder do you want me to open..")
    file_name = SpeechRecognition().lower()

    root_path = [
        "C:\\",
        "D:\\",
        "E:\\"
    ]
    found = False
    for foldername, subfolders, filenames in os.walk(root_path):
        #check folder match
        for subfolder in subfolders:
            if file_name in subfolder.lower():
                os.startfile(os.path.join(foldername, subfolder))
                say(f"Opening Folder {subfolder}") 
                found = True
                return
            
        for filename in filenames:
            if file_name in filename.lower():
                os.startfile(os.path.join(foldername, filename))
                say("Opening file", filename)
                found = True
                return
            
    if not found:
        say("Sorry, I couldn't find any file or folder with that name.")
def close_application(app_name):
    os.system(f"taskkill /f /im {app_name}.exe")

if __name__ == "__main__":
    say("Hello...I am your AI assistant PEPPER")
    wishMe()
    while True:
        if listen_for_wake_word():
            say("Hi Boss... Tell me what should I do on your behalf...")
            text = SpeechRecognition()

            if text:
                if 'pepper' in text:
                    print("Yes Sir")
                    say("Hello Sir.. How's your day..")

                elif 'hello' in text.lower():
                    say("Hello Sir, How can I assist you?")

                elif 'change language to' in text.lower():
                    language = text.lower().replace('change language to', '').strip()
                    change_language(language)

                elif 'tell my emotion' in text or 'emotion' in text.lower():
                    detect_emotion()

                elif 'type' in text: 
                        handle_typing(text)
                
                elif 'who are you' in text:
                    say('My name is Pepper Ports. I can do everything that my creator programmed me to do.')

                elif 'who created you' in text:
                    say("I can't share personal information about my creator, but I was created using Python programming.")

                elif 'search google' in text:
                    say("what should I search ?")
                    query = speech_recognition()
                    if query:
                        for site in sites:
                            if site[0] == "google":
                                search_url = f"{site[1]}/search?q={query}"
                                print(f"Searching Google for: {query}")
                                say(f"Searching Google for: {query}")
                                webbrowser.open(search_url)
                                say(f"Here are the Google search results for {query}")
                                break
                
                elif 'search website' in text.lower():
                    say("Which website do you want me to open?")
                    website_query = text()  # This should capture the next voice input
                    if website_query:
                        print(f"Opening Website: {website_query}")
                        open_website(website_query)
                    else:
                        say("I didn't catch that. Please try again.")

                elif 'search in map' in text.lower():
                    say("which place would you like me to search for you?")
                    place = text.lower().replace("search in map", "").strip()
                    search_google_maps(place)
                    say(f"Searching for {place} in Google Maps")
                    print(f"Searched {place}")

                elif 'search google for' in text:
                    google_search_and_read(text)

                elif "open music" in text:            #music saved in my pc in a folder can be played  -- modify this part to access multiple songs in that very folder.
                   play_music_from_folder()
                
                elif "open video" in text or "show movie" in text:
                    play_video_from_folder()

                elif "open Spotify" in text.lower():
                    spotify_path = "C:\\Users\\LENOVO\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe"
                    os.startfile(spotify_path)

                elif "play music" in text.lower() or "play song" in text.lower():
                    say("What song or video would you like to hear?")
                    song = text()
                    if song:
                        say(f"Searching for {song} on YouTube")
                        
                        # Open new tab and search for music/video on YouTube
                        pyautogui.hotkey('ctrl', 't')  # Open new browser tab
                        pyautogui.typewrite('youtube.com', 0.1)
                        pyautogui.press('enter')

                        time.sleep(3)  # Wait for YouTube to load
                        say("Click on the search bar")
                        pyautogui.moveTo(806, 125, 1)  # Coordinates for YouTube search bar
                        pyautogui.click(x=806, y=125, clicks=1, interval=0, button='left')

                        say(f"Searching for {song} on YouTube")
                        pyautogui.typewrite(song, 0.1)
                        time.sleep(1)
                        say("Press enter")
                        pyautogui.press('enter')

                        time.sleep(3)
                        say("Here are the results on YouTube")

                elif "play music on spotify" in text.lower():
                    say("What song or artist would you like to listen to on Spotify?")
                    song = text()
                    if song:
                        say(f"Searching for {song} on Spotify")

                        time.sleep(3)  # Wait for Spotify to load

                        pyautogui.hotkey('ctrl', 'l')

                        say(f"Searching for {song} on Spotify")
                        pyautogui.typewrite(song, 0.1)
                        time.sleep(1)
                        say("Press enter")
                        pyautogui.press('enter')

                        time.sleep(3)
                        say("Here are the results on Spotify")

                elif 'close spotify' in text:
                    close_application("spotify")
                
                elif 'open tab' in text.lower():
                    pyautogui.hotkey('ctrl', 'T')
                
                elif 'close tab' in text:
                    pyautogui.hotkey('ctrl', 'W')
                
                elif 'open new window' in text:
                    pyautogui.hotkey('ctrl', 'n')
                
                elif 'open incognito window' in text:
                    pyautogui.hotkey('ctrl', 'shift', 'n')
                
                elif 'Open history' in text.lower():
                    pyautogui.hotkey('ctrl', 'h')
                
                elif 'clear browsing history' in text.lower():
                    pyautogui.hotkey('ctrl', 'shift', 'delete')
                
                elif 'previous tab' in text.lower():
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                
                elif 'next tab' in text.lower():
                    pyautogui.hotkey('ctrl', 'tab')
                
                elif 'Open downloads' in text.lower():
                    pyautogui.hotkey('ctrl', 'j')
                
                elif 'select address bar' in text.lower():
                    pyautogui.hotkey('alt', 'd')

                elif "close browser" in text:
                    close_application("msedge")

                elif "close chrome" in text:
                    close_application("chrome")

                elif "time" in text:
                    stateTime = datetime.datetime.now().strftime("%H:%M:%S")
                    print(stateTime)
                    say(f"Sir the time is {stateTime}")

                elif 'open paint' in text:
                    os.startfile("C:\\Windows\\System32\\mspaint.exe")

                elif "draw a rectangle" in text.lower():
                    draw_shape_in_paint("rectangle")
                
                elif "draw a square" in text.lower():
                    draw_shape_in_paint("square")

                elif "draw a circle" in text.lower():
                    draw_shape_in_paint("circle")

                elif 'draw a triangle' in text.lower():
                    draw_shape_in_paint("triangle")

                elif "close paint" in text.lower():
                    close_application("mspaint")

                elif "take screenshot" in text.lower() or "capture the screen" in text.lower():
                    take_screenshot()

                elif 'take a picture' in text.lower() or 'open camera' in text.lower():
                    open_camera("C:\Users\LENOVO\Pictures\Camera Roll")  

                elif 'open notepad' in text:
                    os.startfile("C:\\Windows\\notepad.exe")
                    
                elif 'write in notepad' in text:
                    content = text.replace("write in notepa", "").strip()

                    if content:
                        say("What should be the file name?")
                        filename = text().strip()

                        if filename:
                            if not filename.endswith(".txt"):
                                filename += ".txt"
                            
                            folder_path = "E:\\Mynotes"
                            full_path = os.path.join(folder_path, filename)

                            write_and_save_in_notepad(content, filename)
                        else:
                            write_and_save_in_notepad(content)
                    else:
                        say("No text provided to write.")

                elif 'close notepad' in text:                
                    close_application("notepad")
                
                elif 'what is' in text.lower():
                    say("Searching Wikipedia")
                    text = text.replace('what is', "").strip()
                    try:
                        results = wikipedia.summary(text, sentences=2)
                        say("According to Wikipedia")
                        print(results)
                        say(results)
                    except wikipedia.exceptions.DisambiguationError as e:
                        say("There are multiple results for this query. Please be more specific.")
                    except wikipedia.exceptions.HTTPTimeoutError:
                        say("There was a timeout error while fetching the information from Wikipedia.")
                    except Exception as e:
                        say("Sorry, I couldn't fetch information from Wikipedia.")

                elif 'open command prompt' in text:
                    os.system("start cmd")

                elif 'write in command prompt' in text:
                    pass

                elif 'close command prompt' in text:
                    os.system('taskkill /f /im cmd.exe')
                
                elif 'what is my ip address' in text:
                    say("Checking..")
                    try:
                        ipAdd = requests.get('https://api.ipify.org').text
                        say("The IP address is")
                        print(ipAdd)
                        say(ipAdd)
                    except Exception as e:
                        say("Network is slow. Please try again in some time latter.")

                elif "open file from laptop" in text.lower() or "open folder from laptop" in text.lower():
                    say("Hello Boss...Which file should I open for you..")
                    item_name = text.lower().strip()

                    if item_name:
                        open_file_folder_from_PC(item_name)
                    else:
                        say("I didn't catch the name. Please try again.")

                elif "volume up" in text.lower():
                    control_volume("volume up", 15)
                    say("Increasing the Volume")

                elif "volume down" in text.lower():
                    control_volume("volume down", 15)
                    say("Decreasing the Volume")

                elif "brightness up" in text:
                    control_brightness("brightness up",10)
                    say("Increasing the Brightness")

                elif "brightness down" in text:
                    control_brightness("brightness down",10)
                    say("Decreasing the Brightness")
                
                elif "Undo" in text.lower():
                    pyautogui.hotkey('ctrl', 'Z')
                
                elif "Redo" in text.lower():
                    pyautogui.hotkey('ctrl', 'Y')

                elif "Copy" in text.lower():
                    pyautogui.hotkey('ctrl', 'C')
                
                elif "Paste" in text.lower():
                    pyautogui.hotkey('ctrl', 'V')
                
                elif "Cut" in text.lower() or "remove" in text.lower():
                    pyautogui.hotkey('ctrl', 'X')

                elif "maximize" in text.lower():
                    say("Maximizing the Screen.")
                    pyautogui.hotkey('win', 'up')

                elif "minimize" in text.lower():
                    say("Minimizing the Screen.")
                    pyautogui.hotkey('win', 'down')

                elif "shut down the system" in text:
                    os.system("shutdown /s /t 5")

                elif "restart the system" in text:
                    os.system("shutdown /r /t 5")

                elif "lock the system" in text:
                    os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")

                elif "sleep the system" in text:
                    os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")

                elif "reset chat" in text.lower():
                    chat_history = ""
                    say("Chat memory cleared.")

                elif "Go to sleep" in text:
                    say("Alright then, I am Switching Off.")
                    exit()

                else:
                    response = chat_with_llama(text)
                    say(response)