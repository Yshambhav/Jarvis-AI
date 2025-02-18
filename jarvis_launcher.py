import pystray
from PIL import Image
import os
import threading
import speech_recognition as sr

# Function to wake Jarvis with voice command
def wake_jarvis():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "jarvis wake up" in command:
                    print("Jarvis Activated!")
                    os.system("python jarvis_main.py")  # Run main Jarvis script
                    break
            except sr.UnknownValueError:
                continue

# Function to stop Jarvis from tray
def stop_jarvis(icon, item):
    print("Stopping Jarvis...")
    os._exit(0)

# Load Jarvis system tray icon
image = Image.open("jarvis_icon.png")  # Ensure you have a Jarvis icon file
menu = (("Stop Jarvis", stop_jarvis),)
icon = pystray.Icon("Jarvis", image, "Jarvis AI", menu)

# Run voice activation in a separate thread
threading.Thread(target=wake_jarvis).start()
icon.run()