#!/usr/bin/env python3
# Browser Module - Web-related functionality

import webbrowser
import wikipedia
import requests
from youtube_search import YoutubeSearch
import time
import os
from bs4 import BeautifulSoup

class WebBrowser:
    def __init__(self):
        # Set up the default browser
        self.browser = webbrowser.get()
        
        # Common URLs
        self.urls = {
            'google': 'https://www.google.com/search?q=',
            'youtube': 'https://www.youtube.com/results?search_query=',
            'maps': 'https://www.google.com/maps/search/',
            'images': 'https://www.google.com/search?tbm=isch&q='
        }
    
    def google_search(self, query):
        """Search Google for a query"""
        from modules.speech_engine import SpeechEngine
        speech = SpeechEngine()
        
        search_url = self.urls['google'] + query.replace(' ', '+')
        speech.speak(f"Searching Google for {query}")
        self.browser.open(search_url)
    
    def wikipedia_search(self, query):
        """Search Wikipedia for a query"""
        from modules.speech_engine import SpeechEngine
        speech = SpeechEngine()
        
        try:
            speech.speak(f"Searching Wikipedia for {query}")
            result = wikipedia.summary(query, sentences=3)
            speech.speak("According to Wikipedia:")
            speech.speak(result)
            
            # Open the Wikipedia page in browser
            page = wikipedia.page(query)
            self.browser.open(page.url)
            
        except wikipedia.exceptions.DisambiguationError as e:
            speech.speak("There are multiple results for your query. Please be more specific.")
            options = e.options[:5]  # First 5 options
            speech.speak("Some options are: " + ", ".join(options))
            
        except wikipedia.exceptions.PageError:
            speech.speak(f"Sorry, I couldn't find any Wikipedia page for {query}")
            self.google_search(query)  # Fall back to Google search
            
        except Exception as e:
            speech.speak("I encountered an error while searching Wikipedia.")
            print(f"Wikipedia search error: {e}")
    
    def play_youtube(self, query):
        """Search YouTube and play the first result"""
        from modules.speech_engine import SpeechEngine
        speech = SpeechEngine()
        
        try:
            speech.speak(f"Searching YouTube for {query}")
            
            # Search for videos
            results = YoutubeSearch(query, max_results=1).to_dict()
            
            if results:
                video_id = results[0]['id']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                video_title = results[0]['title']
                
                speech.speak(f"Playing {video_title} on YouTube")
                self.browser.open(video_url)
            else:
                speech.speak(f"Sorry, I couldn't find any YouTube videos for {query}")
                
        except Exception as e:
            speech.speak("I encountered an error while searching YouTube.")
            print(f"YouTube search error: {e}")
    
    def show_images(self, query):
        """Search for images"""
        from modules.speech_engine import SpeechEngine
        speech = SpeechEngine()
        
        search_url = self.urls['images'] + query.replace(' ', '+')
        speech.speak(f"Showing images of {query}")
        self.browser.open(search_url)
    
    def open_maps(self, location):
        """Open Google Maps with a location"""
        from modules.speech_engine import SpeechEngine
        speech = SpeechEngine()
        
        maps_url = self.urls['maps'] + location.replace(' ', '+')
        speech.speak(f"Opening Google Maps for {location}")
        self.browser.open(maps_url)
    
    def get_directions(self, origin=None, destination=None):
        """Get directions from origin to destination"""
        from modules.speech_engine import SpeechEngine
        speech = SpeechEngine()
        
        if not origin:
            speech.speak("What is your starting location?")
            origin = input("Starting location: ")  # For simplicity, using input() instead of speech recognition
        
        if not destination:
            speech.speak("What is your destination?")
            destination = input("Destination: ")
        
        directions_url = f"https://www.google.com/maps/dir/{origin.replace(' ', '+')}/{destination.replace(' ', '+')}"
        speech.speak(f"Getting directions from {origin} to {destination}")
        self.browser.open(directions_url)
    
    def open_website(self, site_name):
        """Open a specific website"""
        from modules.speech_engine import SpeechEngine
        speech = SpeechEngine()
        
        # Dictionary of common websites
        websites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://www.stackoverflow.com',
            'geeksforgeeks': 'https://www.geeksforgeeks.org',
            'codechef': 'https://www.codechef.com',
            'linkedin': 'https://www.linkedin.com'
        }
        
        # Try to find the website
        site_name = site_name.lower()
        if site_name in websites:
            url = websites[site_name]
            speech.speak(f"Opening {site_name}")
            self.browser.open(url)
        else:
            # If not found, try to guess the URL
            speech.speak(f"Opening {site_name}")
            self.browser.open(f"https://www.{site_name}.com")
