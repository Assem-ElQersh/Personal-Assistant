#!/usr/bin/env python3
# PersonalAssistant - Main Entry Point
# Author: Based on work by Roshan Kumar (github.com/roshan9419)

import os
import sys
import time
import random
import datetime
from dotenv import load_dotenv

# Import modules
from modules.speech_engine import SpeechEngine
from modules.security import FaceSecurity
from modules.browser import WebBrowser
from modules.os_functions import SystemFunctions
from modules.utility import Utility
from modules.email_sender import EmailSender
from modules.whatsapp_sender import WhatsAppSender
from modules.calculations import Calculator
from modules.file_operations import FileOperations
from modules.web_automation import WebAutomation
from modules.games import Games
from modules.smart_reply import SmartReply

class PersonalAssistant:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        print("Initializing Personal Assistant...")
        
        # Initialize modules
        self.speech = SpeechEngine()
        self.security = FaceSecurity()
        self.browser = WebBrowser()
        self.system = SystemFunctions()
        self.utility = Utility()
        self.email = EmailSender()
        self.whatsapp = WhatsAppSender()
        self.calculator = Calculator()
        self.file_ops = FileOperations()
        self.web_auto = WebAutomation()
        self.games = Games()
        self.smart_reply = SmartReply()
        
        # Assistant properties
        self.name = "Jarvis"  # You can change the name
        self.user = "User"    # Default user name
        
        # Command history
        self.command_history = []
        
        # Welcome message
        self.speech.speak(f"Hello, I am {self.name}, your personal assistant. How can I help you today?")
    
    def listen(self):
        """Listen for user commands"""
        command = self.speech.recognize_speech()
        if command:
            self.command_history.append(command)
            self.process_command(command)
        return command
    
    def process_command(self, command):
        """Process the command and execute appropriate action"""
        command = command.lower()
        
        # Log the command
        print(f"Command: {command}")
        
        # Check for exit commands
        if "bye" in command or "goodbye" in command or "exit" in command or "quit" in command:
            self.speech.speak(f"Goodbye {self.user}. Have a nice day!")
            sys.exit()
        
        # Basic greeting responses
        elif any(greeting in command for greeting in ["hello", "hi", "hey"]):
            self.speech.speak(f"Hello {self.user}. How can I help you?")
        
        # Time queries
        elif "what time" in command or "current time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speech.speak(f"The current time is {current_time}")
        
        # Date queries
        elif "what date" in command or "what day" in command or "current date" in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speech.speak(f"Today is {current_date}")
        
        # Math calculations
        elif any(term in command for term in ["calculate", "what is", "solve", "computation", "binary of", "factorial", "sin", "cos", "log"]):
            self.calculator.process_calculation(command)
        
        # Web searches
        elif any(term in command for term in ["search for", "search", "look up", "find", "google"]):
            search_query = command.replace("search for", "").replace("search", "").replace("look up", "").replace("find", "").replace("google", "").strip()
            self.browser.google_search(search_query)
        
        # Wikipedia searches
        elif "wikipedia" in command or "who is" in command:
            search_query = command.replace("wikipedia", "").replace("who is", "").strip()
            self.browser.wikipedia_search(search_query)
        
        # YouTube playback
        elif "play" in command and "youtube" in command:
            video_query = command.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
            self.browser.play_youtube(video_query)
        
        # Email functionality
        elif "send an email" in command or "send email" in command:
            self.email.send_email_workflow()
        
        # WhatsApp messaging
        elif "send a whatsapp message" in command or "send whatsapp" in command:
            self.whatsapp.send_whatsapp_workflow()
        
        # File operations
        elif any(term in command for term in ["create a file", "create file", "new file"]):
            if "python" in command:
                self.file_ops.create_file("python")
            elif "java" in command:
                self.file_ops.create_file("java")
            elif "html" in command:
                self.file_ops.create_file("html")
            elif "text" in command or "txt" in command:
                self.file_ops.create_file("text")
            else:
                self.speech.speak("What type of file would you like to create? Python, Java, HTML, or Text?")
        
        # Web automation
        elif "create a html project" in command or "create html project" in command:
            self.web_auto.create_html_project()
        
        # System information
        elif "system information" in command or "system info" in command:
            self.system.get_system_info()
        
        # Battery information
        elif "battery" in command:
            self.system.get_battery_info()
        
        # Take photo/selfie
        elif "take a selfie" in command or "click a photo" in command or "take photo" in command:
            self.system.take_photo()
        
        # Screenshot
        elif "take a screenshot" in command or "screenshot" in command:
            self.system.take_screenshot()
        
        # Volume control
        elif "increase volume" in command or "volume up" in command:
            self.system.adjust_volume("up")
        elif "decrease volume" in command or "volume down" in command:
            self.system.adjust_volume("down")
        elif "mute volume" in command or "mute" in command:
            self.system.adjust_volume("mute")
        elif "full volume" in command or "maximum volume" in command:
            self.system.adjust_volume("max")
        
        # Games
        elif "let's play a game" in command or "play game" in command or "game" in command:
            self.games.choose_game()
        
        # Timer functionality
        elif "set a timer" in command or "timer" in command:
            time_str = command.replace("set a timer for", "").replace("timer for", "").replace("set timer for", "").strip()
            self.utility.set_timer(time_str)
        
        # Weather information
        elif "weather" in command:
            self.utility.get_weather()
        
        # News updates
        elif "news" in command:
            self.utility.get_news()
        
        # Jokes
        elif "joke" in command or "tell me a joke" in command:
            self.utility.tell_joke()
        
        # Todo list
        elif "add to my list" in command or "add to list" in command:
            item = command.replace("add to my list", "").replace("add to list", "").strip()
            self.utility.add_to_todo(item)
        elif "show my list" in command or "show list" in command:
            self.utility.show_todo()
        
        # Handle unknown commands with smart replies
        else:
            self.smart_reply.generate_response(command)
    
    def run(self):
        """Main execution loop"""
        # For additional security, enable the face unlock
        # if self.security.authenticate_face():
        #     self.speech.speak(f"Face authentication successful. Welcome back {self.user}!")
        # else:
        #     self.speech.speak("Face authentication failed. Access denied.")
        #     return
        
        # Main loop
        try:
            while True:
                command = self.listen()
                if not command:
                    # If no command was detected, wait a bit
                    time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nExiting Personal Assistant...")
            self.speech.speak("Goodbye!")

if __name__ == "__main__":
    assistant = PersonalAssistant()
    assistant.run()
