#!/usr/bin/env python3
# Web Automation Module

import os
import datetime
import platform
import random

class WebAutomation:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
        
        # Create directories if they don't exist
        self.projects_dir = os.path.join("assets", "projects")
        os.makedirs(self.projects_dir, exist_ok=True)
        
        # HTML project templates
        self.html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>{title}</h1>
        <nav>
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section>
            <h2>Welcome to {title}</h2>
            <p>This is a starter HTML project created by PersonalAssistant on {date}.</p>
        </section>
        
        <section>
            <h2>About This Project</h2>
            <p>This is a simple HTML, CSS, and JavaScript template to help you get started with your web development project.</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; {year} {title}. All rights reserved.</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>
"""
        
        self.css_template = """/* Main Styles for {title} */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
    padding: 20px;
}

header {
    background-color: #35424a;
    color: white;
    padding: 20px;
    margin-bottom: 20px;
}

header h1 {
    display: inline;
}

nav {
    float: right;
    margin-top: 10px;
}

nav ul {
    list-style: none;
}

nav li {
    display: inline;
    margin-left: 20px;
}

nav a {
    color: white;
    text-decoration: none;
    font-weight: bold;
}

nav a:hover {
    color: #e8491d;
}

section {
    margin-bottom: 30px;
    background: white;
    padding: 20px;
    border-radius: 5px;
}

h2 {
    margin-bottom: 10px;
    color: #35424a;
}

footer {
    text-align: center;
    background-color: #35424a;
    color: white;
    padding: 20px;
    margin-top: 20px;
}

/* Responsive layout */
@media(max-width: 768px) {
    header h1, nav {
        float: none;
        text-align: center;
    }
    
    nav {
        margin-top: 20px;
    }
    
    nav li {
        display: block;
        margin: 10px 0;
    }
}
"""
        
        self.js_template = """// JavaScript for {title}
// Created by PersonalAssistant on {date}

document.addEventListener('DOMContentLoaded', function() {
    console.log('{title} JavaScript loaded');
    
    // You can add your custom JavaScript code here
    
    // Example: Add event listener to navigation links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if(this.getAttribute('href') === '#') {
                e.preventDefault();
                alert('This is a demo link for the ' + this.textContent + ' page');
            }
        });
    });
});
"""
    
    def create_html_project(self):
        """Create a simple HTML project with HTML, CSS, and JavaScript files"""
        # Ask for project name
        self.speech.speak("What would you like to name your HTML project?")
        project_name = input("Project name: ")  # For simplicity, using input() instead of speech recognition
        
        # Create a valid directory name
        dir_name = project_name.strip().replace(" ", "_").lower()
        if not dir_name:
            dir_name = "my_html_project"
        
        # Create project directory path
        project_dir = os.path.join(self.projects_dir, dir_name)
        
        # Check if project already exists
        if os.path.exists(project_dir):
            self.speech.speak(f"A project named {dir_name} already exists. Would you like to overwrite it? Say yes or no.")
            confirmation = input("Overwrite (yes/no): ").lower()  # For simplicity, using input() instead of speech recognition
            
            if confirmation != "yes":
                self.speech.speak("Project creation cancelled.")
                return
        
        try:
            # Create the project directory
            os.makedirs(project_dir, exist_ok=True)
            
            # Get current date and year
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_year = datetime.datetime.now().year
            
            # Create HTML file
            html_content = self.html_template.format(
                title=project_name,
                date=current_date,
                year=current_year
            )
            
            with open(os.path.join(project_dir, "index.html"), "w") as f:
                f.write(html_content)
            
            # Create CSS file
            css_content = self.css_template.format(title=project_name)
            with open(os.path.join(project_dir, "styles.css"), "w") as f:
                f.write(css_content)
            
            # Create JavaScript file
            js_content = self.js_template.format(title=project_name, date=current_date)
            with open(os.path.join(project_dir, "script.js"), "w") as f:
                f.write(js_content)
            
            self.speech.speak(f"HTML project {project_name} created successfully with HTML, CSS, and JavaScript files.")
            self.speech.speak(f"You can find the project at {project_dir}")
            
            # Open the project (optional, works on Windows)
            if platform.system() == "Windows":
                os.startfile(project_dir)
                
        except Exception as e:
            self.speech.speak(f"An error occurred while creating the HTML project: {str(e)}")
            print(f"HTML project creation error: {e}")
