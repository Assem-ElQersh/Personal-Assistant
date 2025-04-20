#!/usr/bin/env python3
# WhatsApp Sender Module

import os
import time
import webbrowser
import re

class WhatsAppSender:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
    
    def validate_phone_number(self, phone):
        """Validate phone number format"""
        # Remove any non-digit characters
        phone = re.sub(r'\D', '', phone)
        
        # Check if the number has a reasonable length (8-15 digits)
        return 8 <= len(phone) <= 15
    
    def send_whatsapp_message(self, phone_number, message):
        """Send a WhatsApp message using the web API"""
        # Format the phone number (remove any non-digit characters)
        phone_number = re.sub(r'\D', '', phone_number)
        
        if not self.validate_phone_number(phone_number):
            self.speech.speak("The phone number format is not valid.")
            return False
        
        try:
            # Create the WhatsApp API URL
            # Note: This uses the web.whatsapp.com API which requires you to be logged in on your browser
            url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
            
            # Open the URL in the default browser
            self.speech.speak("Opening WhatsApp Web. Please wait...")
            webbrowser.open(url)
            
            # Give instructions to the user
            self.speech.speak("WhatsApp Web should open in your browser.")
            self.speech.speak("If you're already logged in, the message will be ready to send.")
            self.speech.speak("Please press Enter in WhatsApp to send the message.")
            
            return True
            
        except Exception as e:
            print(f"Error opening WhatsApp: {e}")
            return False
    
    def send_whatsapp_workflow(self):
        """Interactive workflow for sending a WhatsApp message"""
        self.speech.speak("What is the phone number you want to send a WhatsApp message to?")
        self.speech.speak("Please include the country code.")
        
        phone_number = input("Phone number (with country code): ")  # For simplicity, using input() instead of speech recognition
        
        if not self.validate_phone_number(phone_number):
            self.speech.speak("The phone number format is not valid. Please try again.")
            return
        
        self.speech.speak("What message would you like to send?")
        message = input("Message: ")  # For simplicity, using input() instead of speech recognition
        
        # Confirm before sending
        self.speech.speak(f"I'm about to open WhatsApp to send a message to {phone_number}")
        self.speech.speak("Should I proceed? Say yes or no.")
        
        confirmation = input("Confirm (yes/no): ").lower()  # For simplicity, using input() instead of speech recognition
        
        if confirmation == "yes":
            if self.send_whatsapp_message(phone_number, message):
                self.speech.speak("WhatsApp Web should be open now. Please check your browser.")
            else:
                self.speech.speak("I encountered an error while opening WhatsApp. Please try again.")
        else:
            self.speech.speak("WhatsApp message sending cancelled.")
