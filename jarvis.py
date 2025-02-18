import os
import json
import smtplib
import random
import git
import pywhatkit
import wikipedia
import webbrowser
import threading
import speech_recognition as sr
import pyttsx3
import openai
import pystray
from datetime import datetime
from PIL import Image
from email.message import EmailMessage
from textblob import TextBlob
from flask import Flask, request, jsonify

# Initialize OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initialize Flask App
app = Flask(__name__)

# Text-to-Speech Engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Memory Management
class JarvisMemory:
    def __init__(self):
        self.memory = {}

    def remember(self, key, value):
        self.memory[key] = value

    def recall(self, key):
        return self.memory.get(key, "I don’t remember that yet.")

# Load & Save Memory
def load_memory():
    try:
        with open("jarvis_memory.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_memory(data):
    with open("jarvis_memory.json", "w") as file:
        json.dump(data, file, indent=4)

# User Preferences
memory = load_memory()
def remember_preference(key, value):
    memory[key] = value
    save_memory(memory)
    return f"I will remember that {key} is {value}."

def recall_preference(key):
    return memory.get(key, "I don't remember that yet.")

# Speech Functions
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening for 'Jarvis'...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            if "jarvis" in command:
                return command.replace("jarvis", "").strip()
        except sr.UnknownValueError:
            return ""

# Internet Search
def search_google(query):
    pywhatkit.search(query)
    return f"Searching Google for {query}"

def search_wikipedia(query):
    return wikipedia.summary(query, sentences=1)

def open_website(site_name):
    webbrowser.open(f"https://{site_name}.com")
    return f"Opening {site_name}.com"

# WhatsApp Messaging
def send_whatsapp_message(number, message):
    pywhatkit.sendwhatmsg_instantly(number, message)
    return "WhatsApp message sent!"

# Email Function
def send_email(to_email, subject, message):
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email = EmailMessage()
        email["From"] = sender_email
        email["To"] = to_email
        email["Subject"] = subject
        email.set_content(message)
        server.send_message(email)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {e}"

# AI Chatbot Response
def ask_jarvis(query):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis, a powerful AI assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.route('/ask', methods=['POST'])
def ask_jarvis_api():
    query = request.json["query"]
    response = ask_jarvis(query)
    return jsonify({"response": response})

# Update Jarvis
def update_jarvis():
    repo = git.Repo("path/to/your/JarvisProject")
    repo.remotes.origin.pull()
    os.system("python main.py")
    return "Jarvis updated successfully!"

def check_for_update():
    permission = input("Do you want to update Jarvis? (yes/no): ").lower()
    if permission == "yes":
        update_jarvis()
    else:
        print("Update canceled.")

# Emotion Detection
def detect_emotion(user_input):
    analysis = TextBlob(user_input)
    sentiment_score = analysis.sentiment.polarity
    if sentiment_score > 0.3:
        return "happy"
    elif sentiment_score < -0.3:
        return "sad"
    return "neutral"

# Mood-Based Responses
def get_mood_response(mood):
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "Parallel lines have so much in common. Too bad they’ll never meet."
    ]
    motivation = [
        "Believe in yourself! Every expert was once a beginner.",
        "Stay strong! You’re closer to your goals than you think."
    ]
    if mood == "happy":
        return random.choice(["That's awesome!", "You're on fire today!"])
    elif mood == "sad":
        return random.choice(jokes)
    return random.choice(motivation)

# Process Commands
def process_command(command):
    if not command.lower().startswith("jarvis"):
        return "Please say 'Jarvis' before giving an order."
    if "update yourself" in command:
        check_for_update()
    elif "learn python" in command:
        topic = command.replace("Jarvis learn python", "").strip()
        return ask_jarvis(f"Explain {topic} in Python with an example")
    return "Command executed: " + command

# System Tray Integration
def stop_jarvis(icon, item):
    print("Stopping Jarvis...")
    os._exit(0)

def wake_jarvis():
    with sr.Microphone() as source:
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "jarvis wake up" in command:
                    print("Jarvis Activated!")
                    os.system("python jarvis_main.py")
                    break
            except sr.UnknownValueError:
                continue

image = Image.open("jarvis_icon.png")
menu = ("Stop Jarvis", stop_jarvis)
icon = pystray.Icon("Jarvis", image, "Jarvis AI", menu)
th = threading.Thread(target=wake_jarvis)
th.start()
icon.run()

if __name__ == "__main__":
    app.run(debug=True)
