#!/usr/bin/env python3
# File Operations Module

import os
import datetime
import platform

class FileOperations:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
        
        # Create directories if they don't exist
        self.files_dir = os.path.join("assets", "files")
        os.makedirs(self.files_dir, exist_ok=True)
        
        # File templates
        self.templates = {
            "python": "#!/usr/bin/env python3\n\n# Created by PersonalAssistant\n# Date: {date}\n\ndef main():\n    print(\"Hello, World!\")\n\nif __name__ == \"__main__\":\n    main()\n",
            
            "java": "// Created by PersonalAssistant\n// Date: {date}\n\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}\n",
            
            "html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>My Page</title>\n    <style>\n        body {\n            font-family: Arial, sans-serif;\n            margin: 0;\n            padding: 20px;\n        }\n    </style>\n</head>\n<body>\n    <h1>Hello, World!</h1>\n    <p>This page was created by PersonalAssistant on {date}</p>\n    \n    <script>\n        console.log(\"Page loaded!\");\n    </script>\n</body>\n</html>\n",
            
            "text": "Created by PersonalAssistant\nDate: {date}\n\nThis is a text file.\n"
        }
    
    def create_file(self, file_type):
        """Create a new file of the specified type"""
        # Get the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine file extension and template
        if file_type.lower() == "python":
            extension = ".py"
            template = self.templates["python"]
            
        elif file_type.lower() == "java":
            extension = ".java"
            template = self.templates["java"]
            
        elif file_type.lower() == "html":
            extension = ".html"
            template = self.templates["html"]
            
        elif file_type.lower() == "text":
            extension = ".txt"
            template = self.templates["text"]
            
        else:
            self.speech.speak(f"Sorry, I don't know how to create a {file_type} file.")
            return
        
        # Ask for file name
        self.speech.speak(f"What would you like to name your {file_type} file?")
        filename = input("Filename (without extension): ")  # For simplicity, using input() instead of speech recognition
        
        # Add extension if not provided
        if not filename.endswith(extension):
            filename += extension
        
        # Create the file path
        file_path = os.path.join(self.files_dir, filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            self.speech.speak(f"A file named {filename} already exists. Would you like to overwrite it? Say yes or no.")
            confirmation = input("Overwrite (yes/no): ").lower()  # For simplicity, using input() instead of speech recognition
            
            if confirmation != "yes":
                self.speech.speak("File creation cancelled.")
                return
        
        try:
            # Create the file with the template
            with open(file_path, 'w') as file:
                file.write(template.format(date=current_date))
            
            self.speech.speak(f"{file_type} file created successfully as {filename}")
            
            # Open the file (optional, works on Windows)
            if platform.system() == "Windows":
                os.startfile(file_path)
            else:
                self.speech.speak(f"The file is located at {file_path}")
                
        except Exception as e:
            self.speech.speak(f"An error occurred while creating the file: {str(e)}")
            print(f"File creation error: {e}")
    
    def create_directory(self, directory_name=None):
        """Create a new directory"""
        if not directory_name:
            self.speech.speak("What would you like to name your new directory?")
            directory_name = input("Directory name: ")  # For simplicity, using input() instead of speech recognition
        
        # Create the directory path
        dir_path = os.path.join(self.files_dir, directory_name)
        
        # Check if directory already exists
        if os.path.exists(dir_path):
            self.speech.speak(f"A directory named {directory_name} already exists.")
            return
        
        try:
            # Create the directory
            os.makedirs(dir_path)
            self.speech.speak(f"Directory {directory_name} created successfully")
            
        except Exception as e:
            self.speech.speak(f"An error occurred while creating the directory: {str(e)}")
            print(f"Directory creation error: {e}")
    
    def list_files(self, directory=None):
        """List files in a directory"""
        # Use the files directory if none is specified
        if not directory:
            directory = self.files_dir
        
        try:
            # Get a list of files in the directory
            files = os.listdir(directory)
            
            if not files:
                self.speech.speak(f"The directory {os.path.basename(directory)} is empty.")
                return
            
            # Separate files and directories
            file_list = []
            dir_list = []
            
            for item in files:
                full_path = os.path.join(directory, item)
                if os.path.isfile(full_path):
                    file_list.append(item)
                elif os.path.isdir(full_path):
                    dir_list.append(item)
            
            # Speak the results
            self.speech.speak(f"In the directory {os.path.basename(directory)}, I found:")
            
            if dir_list:
                self.speech.speak(f"{len(dir_list)} directories: {', '.join(dir_list)}")
            
            if file_list:
                self.speech.speak(f"{len(file_list)} files: {', '.join(file_list)}")
                
        except Exception as e:
            self.speech.speak(f"An error occurred while listing files: {str(e)}")
            print(f"File listing error: {e}")
