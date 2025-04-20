#!/usr/bin/env python3
# Speech Engine Module

import pyttsx3
import speech_recognition as sr
import random

class SpeechEngine:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Set properties
        self.engine.setProperty('rate', 180)  # Speed of speech
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Set default voice (index 0 is usually male, 1 is female)
        self.engine.setProperty('voice', voices[0].id)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate recognizer for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Response variations for when speech isn't understood
        self.not_understood_responses = [
            "I'm sorry, I didn't catch that.",
            "Could you please repeat that?",
            "I didn't understand what you said.",
            "Sorry, I couldn't understand your command.",
            "I'm having trouble understanding you."
        ]
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def recognize_speech(self):
        """Convert speech to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text
            
        except sr.WaitTimeoutError:
            # Timeout occurred while waiting for phrase to start
            print("Timeout: No speech detected")
            return None
            
        except sr.UnknownValueError:
            # Speech was unintelligible
            response = random.choice(self.not_understood_responses)
            self.speak(response)
            return None
            
        except sr.RequestError as e:
            # Could not request results from Google Speech Recognition service
            error_msg = f"Could not request results from Google Speech Recognition service; {e}"
            print(error_msg)
            self.speak("I'm having trouble connecting to my speech recognition service.")
            return None
            
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            self.speak("I encountered an error with speech recognition.")
            return None
    
    def change_voice(self, gender="male"):
        """Change the voice of the assistant"""
        voices = self.engine.getProperty('voices')
        if gender.lower() == "female":
            self.engine.setProperty('voice', voices[1].id)
            self.speak("I've changed to a female voice.")
        else:
            self.engine.setProperty('voice', voices[0].id)
            self.speak("I've changed to a male voice.")
