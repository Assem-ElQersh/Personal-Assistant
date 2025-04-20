#!/usr/bin/env python3
# Email Sender Module

import smtplib
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

class EmailSender:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
        
        # Load environment variables for email credentials
        load_dotenv()
        self.email_address = os.getenv('MAIL_USERNAME')
        self.email_password = os.getenv('MAIL_PASSWORD')
        
        # Check if credentials are available
        if not self.email_address or not self.email_password:
            print("Warning: Email credentials not found in .env file")
    
    def validate_email(self, email):
        """Validate email address format"""
        # Simple email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def send_email(self, to_email, subject, message):
        """Send an email"""
        if not self.email_address or not self.email_password:
            self.speech.speak("Email credentials are not configured. Please set up your email credentials in the .env file.")
            return False
        
        if not self.validate_email(to_email):
            self.speech.speak("The email address you provided is not valid.")
            return False
        
        try:
            # Create the email
            email = MIMEMultipart()
            email["From"] = self.email_address
            email["To"] = to_email
            email["Subject"] = subject
            
            # Attach the message
            email.attach(MIMEText(message, "plain"))
            
            # Connect to the SMTP server
            # Note: Different email providers have different SMTP settings
            # Below is for Gmail, you might need to modify for other providers
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Secure the connection
                server.login(self.email_address, self.email_password)
                server.send_message(email)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_email_workflow(self):
        """Interactive workflow for sending an email"""
        self.speech.speak("Who would you like to send an email to?")
        to_email = input("Recipient's email: ")  # For simplicity, using input() instead of speech recognition
        
        if not self.validate_email(to_email):
            self.speech.speak("The email address is not valid. Please try again.")
            return
        
        self.speech.speak("What is the subject of your email?")
        subject = input("Subject: ")  # For simplicity, using input() instead of speech recognition
        
        self.speech.speak("What message would you like to send?")
        message = input("Message: ")  # For simplicity, using input() instead of speech recognition
        
        # Confirm before sending
        self.speech.speak(f"I'm about to send an email to {to_email} with the subject: {subject}")
        self.speech.speak("Should I send it? Say yes or no.")
        
        confirmation = input("Confirm (yes/no): ").lower()  # For simplicity, using input() instead of speech recognition
        
        if confirmation == "yes":
            self.speech.speak("Sending email...")
            
            if self.send_email(to_email, subject, message):
                self.speech.speak("Email sent successfully!")
            else:
                self.speech.speak("I encountered an error while sending the email. Please check your credentials and try again.")
        else:
            self.speech.speak("Email sending cancelled.")
