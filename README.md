# Personal Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

A versatile, voice-controlled personal assistant built in Python. This project offers many functionalities, including web searches, file operations, email sending, games, and more.

![Personal Assistant](assets/images/thumbnail.jpg)

## Features

PersonalAssistant can perform numerous tasks through simple voice commands, including:

### Information & Web
- 🔍 Web searches (Google, Wikipedia)
- 📺 Play videos from YouTube
- 🌦️ Weather reports
- 📰 News updates
- 🌐 Open websites
- 🗺️ Get directions and show locations on maps

### Communication
- 📧 Send emails
- 💬 Send WhatsApp messages

### System Operations
- 📁 Create files (Python, Java, HTML, etc.)
- 🖥️ System information and battery status
- 📸 Take photos using webcam
- 📊 Take screenshots
- 🔊 Volume control

### Productivity & Entertainment
- 🧮 Perform math calculations
- ⏰ Set timers
- 📝 Manage to-do lists
- 🎮 Play games like Rock Paper Scissors
- 🎲 Coin toss and dice roll

### Web Development
- 🌐 Create HTML projects with CSS and JavaScript templates

### Security
- 🔒 Face recognition (optional authentication)

## Requirements

- Python 3.8 or higher
- Windows OS (some features are Windows-specific)
- Webcam (for photo/security features)
- Microphone (for voice commands)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Assem-ElQersh/Personal-Assistant.git
   cd PersonalAssistant
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```
   cp .env.template .env
   ```
   Then edit the `.env` file with your email credentials and API keys.

## Usage

1. Start the assistant:
   ```
   python main.py
   ```

2. Speak commands after the assistant greets you. Some example commands:

### Web & Information
- "Search for artificial intelligence news"
- "Play Taylor Swift music on YouTube"
- "Show me images of national parks"
- "What is the weather today?"
- "Give me some news"
- "Who is Albert Einstein?"

### System Control
- "Take a selfie"
- "Take a screenshot"
- "Increase the volume"
- "Give my system information"
- "What's my battery life"

### Productivity
- "Create a Python file"
- "Create an HTML project"
- "Set a timer for 5 minutes"
- "Add 'Buy groceries' to my list"
- "Show my list"

### Math
- "What is 245 plus 567?"
- "What is the binary of 142?"
- "What is the value of factorial 10?"
- "What is the value of sine 90?"

### Communication
- "Send an email"
- "Send a WhatsApp message"

### Entertainment
- "Let's play a game"
- "Tell me a joke"
- "Toss a coin"
- "Roll a dice"

## Project Structure

```
PersonalAssistant/
├── main.py                  # Main entry point
├── requirements.txt         # Dependencies list
├── .env                     # Environment variables (create from template)
├── modules/
│   ├── __init__.py
│   ├── speech_engine.py     # Text-to-speech and speech recognition
│   ├── security.py          # Face recognition for authentication
│   ├── browser.py           # Web-related functionality
│   ├── os_functions.py      # OS level operations
│   ├── utility.py           # Utility functions
│   ├── email_sender.py      # Email functionality
│   ├── whatsapp_sender.py   # WhatsApp messaging
│   ├── calculations.py      # Math operations
│   ├── file_operations.py   # File operations
│   ├── web_automation.py    # Web automation functions
│   ├── games.py             # Games implementation
│   └── smart_reply.py       # Smart response functions
└── assets/
    ├── face_data/           # Store face recognition data
    ├── images/              # Images for UI
    ├── screenshots/         # Saved screenshots
    ├── photos/              # Saved photos
    ├── files/               # Created files
    ├── projects/            # Web projects
    └── data/                # Application data
```

## Extending the Assistant

You can extend the assistant's functionality by:

1. Adding new methods to existing modules
2. Creating new modules for specialized tasks
3. Enhancing the command recognition in `main.py`

Refer to the modular structure to understand how to implement new features.

## API Keys

For some features, you'll need API keys:

- Weather information: [OpenWeatherMap API](https://openweathermap.org/api)
- News updates: [NewsAPI](https://newsapi.org/)

Add these to your `.env` file.

## Troubleshooting

Common issues:

- **Speech recognition not working**: Check your microphone settings and ensure you have a working internet connection.
- **PyAudio installation errors**: On Windows, you might need to download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).
- **Email sending fails**: For Gmail, you need to use an App Password. Enable 2FA and generate an App Password from your Google Account.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Assem-ElQersh/Personal-Assistant/blob/main/LICENSE) file for details.

## Acknowledgments

- This project was inspired by [Roshan Kumar's original PersonalAssistant](https://github.com/roshan9419/PersonalAssistantChatbot)

---

Made with ❤️ by [Assem ElQersh](https://assem-elqersh.github.io/)
