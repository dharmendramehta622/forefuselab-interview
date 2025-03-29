import openai  # Using OpenAI's API for AI-driven journaling prompts and responses
import speech_recognition as sr  # Library for speech-to-text conversion
from datetime import datetime

class SmartJournal:
    def __init__(self, user_id):
        """
        Initialize the smart journal system for a user.
        :param user_id: Unique identifier for the user
        """
        self.user_id = user_id  # Store the user ID
        self.entries = []  # List to store journal entries
        self.prompts = ["How are you feeling today?", "What was the highlight of your day?"]  # Default prompts
    
    def generate_ai_prompt(self, context=""):
        """
        Generate an AI-driven prompt based on user context.
        :param context: Additional context such as stress levels, recent events, etc.
        """
        prompt = f"Generate a thoughtful journaling question based on the following context: {context}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    
    def transcribe_voice_note(self, audio_file):
        """
        Convert speech to text using Whisper (or another STT model).
        :param audio_file: Path to the audio file
        """
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)  # Using Google's API for now
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Speech recognition service unavailable."
    
    def add_entry(self, text):
        """
        Add a journal entry.
        :param text: The journal text written or transcribed
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entries.append({"timestamp": timestamp, "text": text})
        return "Entry added successfully!"
    
    def summarize_day(self):
        """
        Generate key insights from the user's journal entries for the day.
        """
        journal_texts = " ".join([entry["text"] for entry in self.entries])
        prompt = f"Summarize the key insights from the following journal entries: {journal_texts}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
