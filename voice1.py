import speech_recognition as sr
import pyttsx3
import pyautogui
import time
import subprocess
import webbrowser
import wikipedia
import threading

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize recognizer
recognizer = sr.Recognizer()


speak("Hello, how can I help you?")

# Function to recognize speech
def recognize_speech_from_mic(duration=4):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        speak("Listening...")
        print("Listening...")
        audio = recognizer.listen(source, timeout=duration)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            speak(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Request error.")
            return None

def open_icon(command):
    icon_x, icon_y = 100, 100
    if "browser" in command.lower() or "calculator" in command.lower() or "notepad" in command.lower():
        pyautogui.click(icon_x, icon_y)

def open_website(url):
    webbrowser.open(url)
    speak(f"Opening {url}")

def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    speak(f"According to Wikipedia, {results}")

# Function to execute commands
def execute_command(command):
    if "move cursor" in command:
        try:
            direction, distance = command.split(" ")[2], int(command.split(" ")[3])
            if direction == "left":
                pyautogui.moveRel(-distance, 0, duration=0.25)
            elif direction == "right":
                pyautogui.moveRel(distance, 0, duration=0.25)
            elif direction == "up":
                pyautogui.moveRel(0, -distance, duration=0.25)
            elif direction == "down":
                pyautogui.moveRel(0, distance, duration=0.25)
        except:
            print("Invalid move mouse command")
    
    elif "open website" in command:
        speak("Which website would you like to open?")
        website = recognize_speech_from_mic()
        open_website(f"https://{website}")
    
    elif "search wikipedia for" in command:
        query = command.replace("search wikipedia for", "").strip()
        search_wikipedia(query)
    
    elif "click" in command:
        pyautogui.click()
    
    elif "double click" in command:
        pyautogui.doubleClick()
    
    elif "right click" in command:
        pyautogui.rightClick()
    
    elif "minimise window" in command:
        pyautogui.hotkey('win', 'down')
    
    elif "maximize window" in command:
        pyautogui.hotkey('win', 'up')
    
    elif "close window" in command:
        pyautogui.hotkey('alt', 'f4')
    
    elif "explorer" in command:
        pyautogui.hotkey('win', 'e')
    
    elif "increase volume" in command:
        pyautogui.press('volumeup')
    
    elif "decrease volume" in command:
        pyautogui.press('volumedown')
    
    elif "scroll up" in command:
        pyautogui.scroll(100)
        print("Scrolling up")
    
    elif "scroll down" in command:
        pyautogui.scroll(-100)
        print("Scrolling down")
    
    elif "select" in command:
        pyautogui.mouseDown()
        pyautogui.moveTo(500, 500, duration=1)
        pyautogui.mouseUp()
    
    elif "all" in command:
        pyautogui.hotkey('ctrl', 'a')
    
    elif "copy" in command:
        pyautogui.hotkey('ctrl', 'c')
    
    elif "paste" in command:
        pyautogui.hotkey('ctrl', 'v')
    
    elif "save" in command:
        pyautogui.hotkey('ctrl', 's')
    
    else:
        print("Unknown command")

# Function to reset recognizer to prevent slow down
def reset_recognizer():
    global recognizer
    recognizer = sr.Recognizer()

# Main loop
def main():
    reset_count = 0
    while True:
        command = recognize_speech_from_mic(4)
        if command:
            command_thread = threading.Thread(target=execute_command, args=(command,))
            command_thread.start()
        reset_count += 1
        if reset_count >= 5:  # Reset recognizer every 5 commands to prevent slow down
            reset_recognizer()
            reset_count = 0

if __name__ == "__main__":
    main()
