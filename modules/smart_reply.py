#!/usr/bin/env python3
# Smart Reply Module

import random
import datetime
import re

class SmartReply:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
        
        # General responses for different types of queries
        self.greetings = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Greetings! How may I assist you?",
            "Hey! I'm here to help. What do you need?"
        ]
        
        self.farewells = [
            "Goodbye! Have a great day!",
            "Bye! Call me if you need anything.",
            "See you later! Take care!",
            "Farewell! It was nice talking to you."
        ]
        
        self.thank_you_responses = [
            "You're welcome!",
            "Happy to help!",
            "My pleasure!",
            "No problem at all!"
        ]
        
        self.apology_responses = [
            "It's alright, no need to apologize.",
            "No worries at all.",
            "That's okay, don't worry about it.",
            "No problem, I understand."
        ]
        
        self.unknown_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "I don't have enough information to help with that.",
            "I'm still learning about that topic.",
            "I'm afraid I don't know how to help with that yet."
        ]
        
        self.identity_responses = [
            "I'm your personal assistant, designed to help you with various tasks.",
            "I'm an AI assistant created to make your life easier.",
            "Think of me as your digital helper, ready to assist with what you need.",
            "I'm your virtual assistant, always ready to help!"
        ]
        
        self.capability_responses = [
            "I can help you with tasks like web searches, playing videos, sending emails, creating files, and much more!",
            "I can search the web, play YouTube videos, send emails, create files, and provide information on various topics.",
            "I'm designed to assist with searches, media playback, communications, file creation, and answering questions.",
            "I can perform many tasks including searches, playing media, sending messages, file operations, and providing information."
        ]
        
        self.compliment_responses = [
            "Thank you! I'm happy to hear that.",
            "That's very kind of you to say!",
            "I appreciate your feedback!",
            "Thanks! I'm glad I could be helpful."
        ]
        
        # Specific topic responses
        self.about_responses = {
            "birthday": "I don't have a birthday in the traditional sense. I was created by my developers, but I don't age like humans do.",
            "name": "My name is Jarvis, your personal assistant.",
            "creator": "I was created based on Roshan Kumar's PersonalAssistant project, but I've been rebuilt to help you.",
            "favorite": "As an AI assistant, I don't have personal preferences, but I'm always happy to help you with whatever you need!",
            "live": "I exist as a software program running on your computer. I don't have a physical presence like humans do.",
            "age": "I don't have an age in the traditional sense. I'm a software program that was recently set up for you."
        }
    
    def generate_response(self, query):
        """Generate a smart response based on the query type"""
        query = query.lower()
        
        # Check for greetings
        if any(greeting in query for greeting in ["hello", "hi", "hey", "greetings"]):
            self.speech.speak(random.choice(self.greetings))
            return
        
        # Check for farewells
        elif any(farewell in query for farewell in ["bye", "goodbye", "see you", "farewell"]):
            self.speech.speak(random.choice(self.farewells))
            return
        
        # Check for thank you
        elif any(thanks in query for thanks in ["thank you", "thanks", "appreciate it"]):
            self.speech.speak(random.choice(self.thank_you_responses))
            return
        
        # Check for apologies
        elif any(apology in query for apology in ["sorry", "apologize", "my fault"]):
            self.speech.speak(random.choice(self.apology_responses))
            return
        
        # Check for identity questions
        elif any(identity in query for identity in ["who are you", "what are you", "your name"]):
            self.speech.speak(random.choice(self.identity_responses))
            return
        
        # Check for capability questions
        elif any(capability in query for capability in ["what can you do", "your abilities", "help me with", "capable of"]):
            self.speech.speak(random.choice(self.capability_responses))
            return
        
        # Check for compliments
        elif any(compliment in query for compliment in ["good job", "well done", "you're great", "you're amazing", "smart", "clever"]):
            self.speech.speak(random.choice(self.compliment_responses))
            return
        
        # Check for specific topic questions
        elif "birthday" in query or "born" in query:
            self.speech.speak(self.about_responses["birthday"])
            return
        elif "your name" in query:
            self.speech.speak(self.about_responses["name"])
            return
        elif "creator" in query or "who made you" in query:
            self.speech.speak(self.about_responses["creator"])
            return
        elif "favorite" in query or "like best" in query:
            self.speech.speak(self.about_responses["favorite"])
            return
        elif "where do you live" in query or "where are you" in query:
            self.speech.speak(self.about_responses["live"])
            return
        elif "how old" in query or "your age" in query:
            self.speech.speak(self.about_responses["age"])
            return
        
        # Check for time queries
        elif "current time" in query or "time now" in query or "what time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speech.speak(f"The current time is {current_time}")
            return
        
        # Check for date queries
        elif "today's date" in query or "what day" in query or "what date" in query:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speech.speak(f"Today is {current_date}")
            return
        
        # Default response for unknown queries
        else:
            self.speech.speak(random.choice(self.unknown_responses))
            self.speech.speak("I can help you with web searches, playing videos, sending emails, creating files, and more. Just let me know what you need.")
            return
