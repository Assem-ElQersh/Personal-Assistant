#!/usr/bin/env python3
# Utility Module - Miscellaneous helper functions

import os
import json
import random
import time
import threading
import requests
from datetime import datetime
import re

class Utility:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
        
        # Create directories if they don't exist
        self.data_dir = os.path.join("assets", "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize todo list file
        self.todo_file = os.path.join(self.data_dir, "todo_list.json")
        if not os.path.exists(self.todo_file):
            with open(self.todo_file, 'w') as f:
                json.dump([], f)
        
        # OpenWeatherMap API key (you'll need to sign up for one)
        self.weather_api_key = os.getenv('WEATHER_API_KEY', '')
        
        # News API key (you'll need to sign up for one)
        self.news_api_key = os.getenv('NEWS_API_KEY', '')
        
        # Jokes list
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Why was six afraid of seven? Because seven eight nine!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "What do you call a fake noodle? An impasta!",
            "How do you organize a space party? You planet!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "I'm reading a book on anti-gravity. It's impossible to put down!",
            "Did you hear about the guy who invented the knock-knock joke? He won the 'no-bell' prize!",
            "I used to be a baker, but I couldn't make enough dough."
        ]
    
    def set_timer(self, time_str):
        """Set a timer for a specified amount of time"""
        # Extract time components
        minutes, seconds = 0, 0
        
        # Try to parse the time string
        if "minute" in time_str and "second" in time_str:
            match = re.search(r'(\d+)\s*minute.*?(\d+)\s*second', time_str)
            if match:
                minutes, seconds = int(match.group(1)), int(match.group(2))
        elif "minute" in time_str:
            match = re.search(r'(\d+)\s*minute', time_str)
            if match:
                minutes = int(match.group(1))
        elif "second" in time_str:
            match = re.search(r'(\d+)\s*second', time_str)
            if match:
                seconds = int(match.group(1))
        else:
            # Try to directly extract numbers
            numbers = re.findall(r'\d+', time_str)
            if len(numbers) == 1:
                # Assume seconds if just one number
                seconds = int(numbers[0])
            elif len(numbers) >= 2:
                # Assume minutes and seconds if two or more numbers
                minutes, seconds = int(numbers[0]), int(numbers[1])
        
        # Calculate total seconds
        total_seconds = minutes * 60 + seconds
        
        if total_seconds <= 0:
            self.speech.speak("I couldn't understand the time. Please try again.")
            return
        
        # Speak confirmation
        time_msg = ""
        if minutes > 0:
            time_msg += f"{minutes} minute{'s' if minutes != 1 else ''}"
        if seconds > 0:
            if time_msg:
                time_msg += " and "
            time_msg += f"{seconds} second{'s' if seconds != 1 else ''}"
        
        self.speech.speak(f"Setting a timer for {time_msg}")
        
        # Start the timer in a separate thread
        timer_thread = threading.Thread(target=self._run_timer, args=(total_seconds,))
        timer_thread.daemon = True
        timer_thread.start()
    
    def _run_timer(self, seconds):
        """Run the timer in a separate thread"""
        time.sleep(seconds)
        self.speech.speak("Timer is up! Timer is up!")
        
        # Additional alerts
        for _ in range(2):
            time.sleep(1)
            self.speech.speak("Your timer has finished!")
    
    def get_weather(self, city=None):
        """Get current weather information"""
        if not self.weather_api_key:
            self.speech.speak("Weather API key is not configured. Please set up your OpenWeatherMap API key.")
            return
        
        if not city:
            self.speech.speak("What city would you like the weather for?")
            city = input("City: ")  # For simplicity, using input() instead of speech recognition
        
        try:
            # Make API request
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                # Extract weather information
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                desc = data['weather'][0]['description']
                wind_speed = data['wind']['speed']
                
                # Prepare and speak weather report
                weather_report = f"Current weather in {city}: {desc}. "
                weather_report += f"The temperature is {temp:.1f}°C, but it feels like {feels_like:.1f}°C. "
                weather_report += f"Humidity is {humidity}% and wind speed is {wind_speed} meters per second."
                
                self.speech.speak(weather_report)
            else:
                # Handle errors
                if response.status_code == 404:
                    self.speech.speak(f"I couldn't find weather information for {city}. Please check the city name.")
                else:
                    self.speech.speak("I couldn't retrieve the weather information. Please try again later.")
                
        except Exception as e:
            self.speech.speak("An error occurred while fetching the weather information.")
            print(f"Weather API error: {e}")
    
    def get_news(self, category=None):
        """Get the latest news headlines"""
        if not self.news_api_key:
            self.speech.speak("News API key is not configured. Please set up your News API key.")
            return
        
        categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
        
        if not category:
            self.speech.speak("What category of news would you like? Business, entertainment, health, science, sports, or technology?")
            category = input("Category: ").lower()  # For simplicity, using input() instead of speech recognition
        
        if category not in categories:
            category = "general"
        
        try:
            # Make API request
            url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "ok":
                articles = data["articles"]
                
                if articles:
                    self.speech.speak(f"Here are the top {min(5, len(articles))} {category} news headlines:")
                    
                    for i, article in enumerate(articles[:5]):
                        headline = article["title"]
                        source = article["source"]["name"]
                        
                        self.speech.speak(f"Headline {i+1}: {headline}. From: {source}")
                        time.sleep(0.5)  # Pause between headlines
                    
                    # Ask if user wants to hear more about any headline
                    self.speech.speak("Would you like me to tell you more about any of these headlines? If yes, say the headline number.")
                else:
                    self.speech.speak(f"I couldn't find any {category} news headlines at the moment.")
            else:
                self.speech.speak("I couldn't retrieve the news. Please try again later.")
                
        except Exception as e:
            self.speech.speak("An error occurred while fetching the news.")
            print(f"News API error: {e}")
    
    def tell_joke(self):
        """Tell a random joke"""
        joke = random.choice(self.jokes)
        self.speech.speak(joke)
    
    def add_to_todo(self, item):
        """Add an item to the todo list"""
        if not item:
            self.speech.speak("What would you like to add to your list?")
            item = input("Todo item: ")  # For simplicity, using input() instead of speech recognition
        
        try:
            # Load existing todo list
            with open(self.todo_file, 'r') as f:
                todo_list = json.load(f)
            
            # Add new item with timestamp
            new_item = {
                "item": item,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completed": False
            }
            
            todo_list.append(new_item)
            
            # Save updated list
            with open(self.todo_file, 'w') as f:
                json.dump(todo_list, f, indent=4)
            
            self.speech.speak(f"Added to your list: {item}")
            
        except Exception as e:
            self.speech.speak("An error occurred while updating your todo list.")
            print(f"Todo list error: {e}")
    
    def show_todo(self):
        """Show the current todo list"""
        try:
            # Load todo list
            with open(self.todo_file, 'r') as f:
                todo_list = json.load(f)
            
            if not todo_list:
                self.speech.speak("Your todo list is empty.")
                return
            
            # Filter incomplete items
            incomplete_items = [item for item in todo_list if not item["completed"]]
            
            if not incomplete_items:
                self.speech.speak("You've completed all items on your todo list. Congratulations!")
                return
            
            # Speak todo items
            self.speech.speak(f"You have {len(incomplete_items)} items on your todo list:")
            
            for i, item in enumerate(incomplete_items):
                self.speech.speak(f"Item {i+1}: {item['item']}")
                time.sleep(0.3)  # Pause between items
                
        except Exception as e:
            self.speech.speak("An error occurred while reading your todo list.")
            print(f"Todo list error: {e}")
    
    def coin_toss(self):
        """Simulate a coin toss"""
        result = random.choice(["heads", "tails"])
        self.speech.speak(f"I flipped a coin and got: {result}")
        return result
    
    def roll_dice(self, sides=6):
        """Roll a dice with the specified number of sides"""
        if sides < 2:
            self.speech.speak("A dice must have at least 2 sides.")
            return None
        
        result = random.randint(1, sides)
        self.speech.speak(f"I rolled a {sides}-sided dice and got: {result}")
        return result
