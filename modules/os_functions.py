#!/usr/bin/env python3
# OS Functions Module - System-level operations

import os
import sys
import platform
import psutil
import cv2
import time
import pyscreenshot as ImageGrab
from datetime import datetime
import subprocess

class SystemFunctions:
    def __init__(self):
        # Import speech engine
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
        
        # Create directories if they don't exist
        self.screenshots_dir = os.path.join("assets", "screenshots")
        self.photos_dir = os.path.join("assets", "photos")
        
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.photos_dir, exist_ok=True)
        
        # Set Windows-specific commands
        if platform.system() == "Windows":
            self.volume_commands = {
                "up": "nircmd.exe changesysvolume 10000",
                "down": "nircmd.exe changesysvolume -10000",
                "mute": "nircmd.exe mutesysvolume 1",
                "unmute": "nircmd.exe mutesysvolume 0",
                "max": "nircmd.exe setsysvolume 65535"
            }
    
    def get_system_info(self):
        """Get and speak system information"""
        # Get system information
        system = platform.system()
        processor = platform.processor()
        architecture = platform.architecture()[0]
        hostname = platform.node()
        
        # Get memory information
        memory = psutil.virtual_memory()
        total_memory = f"{memory.total / (1024 ** 3):.2f} GB"
        available_memory = f"{memory.available / (1024 ** 3):.2f} GB"
        
        # Get disk information
        disk = psutil.disk_usage('/')
        total_disk = f"{disk.total / (1024 ** 3):.2f} GB"
        free_disk = f"{disk.free / (1024 ** 3):.2f} GB"
        
        # Prepare the system information message
        system_info = f"""
        Operating System: {system}
        Processor: {processor}
        Architecture: {architecture}
        Hostname: {hostname}
        Total Memory: {total_memory}
        Available Memory: {available_memory}
        Total Disk Space: {total_disk}
        Free Disk Space: {free_disk}
        """
        
        # Print and speak system information
        print(system_info)
        self.speech.speak(f"Your system is running {system} with a {processor} processor.")
        self.speech.speak(f"You have {total_memory} of total memory with {available_memory} available.")
        self.speech.speak(f"Your disk has {total_disk} of total space with {free_disk} free.")
    
    def get_battery_info(self):
        """Get and speak battery information"""
        if not hasattr(psutil, "sensors_battery"):
            self.speech.speak("Battery information is not available on this system.")
            return
        
        battery = psutil.sensors_battery()
        if battery is None:
            self.speech.speak("No battery detected. You might be using a desktop computer.")
            return
        
        percent = battery.percent
        power_plugged = battery.power_plugged
        
        status = "plugged in" if power_plugged else "on battery power"
        
        # Determine battery status
        if percent >= 75:
            level = "high"
        elif percent >= 40:
            level = "moderate"
        elif percent >= 15:
            level = "low"
        else:
            level = "very low"
        
        # Speak battery information
        self.speech.speak(f"Your battery is at {percent} percent, which is {level}. Your device is currently {status}.")
        
        # Add warning for low battery
        if percent <= 15 and not power_plugged:
            self.speech.speak("Warning: Battery level is critically low. Please connect to a power source soon.")
    
    def take_photo(self):
        """Take a photo using the webcam"""
        try:
            # Open webcam
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.speech.speak("I couldn't access the webcam.")
                return
            
            # Warm up the camera
            self.speech.speak("Preparing to take a photo...")
            for _ in range(3):
                ret, frame = cap.read()
                time.sleep(0.1)
            
            # Take the actual photo
            self.speech.speak("Say cheese!")
            time.sleep(1)
            ret, frame = cap.read()
            
            # Release the webcam
            cap.release()
            
            if not ret:
                self.speech.speak("I couldn't capture the photo.")
                return
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.photos_dir, f"photo_{timestamp}.jpg")
            
            # Save the photo
            cv2.imwrite(filename, frame)
            self.speech.speak(f"Photo taken and saved as {os.path.basename(filename)}")
            
            # Show the photo (optional, works on Windows)
            if platform.system() == "Windows":
                os.startfile(filename)
            
        except Exception as e:
            self.speech.speak("An error occurred while taking the photo.")
            print(f"Error taking photo: {e}")
    
    def take_screenshot(self):
        """Take a screenshot of the current screen"""
        try:
            # Take the screenshot
            self.speech.speak("Taking a screenshot...")
            screenshot = ImageGrab.grab()
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.screenshots_dir, f"screenshot_{timestamp}.png")
            
            # Save the screenshot
            screenshot.save(filename)
            self.speech.speak(f"Screenshot taken and saved as {os.path.basename(filename)}")
            
            # Show the screenshot (optional, works on Windows)
            if platform.system() == "Windows":
                os.startfile(filename)
            
        except Exception as e:
            self.speech.speak("An error occurred while taking the screenshot.")
            print(f"Error taking screenshot: {e}")
    
    def adjust_volume(self, direction):
        """Adjust system volume (up, down, mute, max)"""
        # Check if we're on Windows
        if platform.system() != "Windows":
            self.speech.speak("Volume control is currently only supported on Windows.")
            return
        
        try:
            if direction.lower() == "up":
                # Increase volume
                self.speech.speak("Increasing volume")
                os.system(self.volume_commands["up"])
                
            elif direction.lower() == "down":
                # Decrease volume
                self.speech.speak("Decreasing volume")
                os.system(self.volume_commands["down"])
                
            elif direction.lower() == "mute":
                # Mute volume
                self.speech.speak("Muting volume")
                os.system(self.volume_commands["mute"])
                
            elif direction.lower() == "max":
                # Maximum volume
                self.speech.speak("Setting volume to maximum")
                os.system(self.volume_commands["max"])
                
            else:
                self.speech.speak("Invalid volume command")
                
        except Exception as e:
            self.speech.speak("An error occurred while adjusting the volume.")
            print(f"Error adjusting volume: {e}")

