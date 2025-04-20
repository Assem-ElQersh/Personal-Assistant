#!/usr/bin/env python3
# Games Module

import random
import time
import tkinter as tk
from tkinter import messagebox, Button, Label, PhotoImage, Frame
import os
import webbrowser

class Games:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
        
        # URLs for online games
        self.online_games = {
            "Tic Tac Toe": "https://playtictactoe.org/",
            "Chess": "https://www.chess.com/play/online",
            "2048": "https://play2048.co/",
            "Sudoku": "https://sudoku.com/",
            "Tetris": "https://tetris.com/play-tetris",
            "Snake": "https://playsnake.org/"
        }
    
    def choose_game(self):
        """Present game options to the user"""
        self.speech.speak("Which game would you like to play?")
        self.speech.speak("I have Rock Paper Scissors or I can open online games for you.")
        
        game_choice = input("Choose a game: ").lower()  # For simplicity, using input() instead of speech recognition
        
        if "rock" in game_choice or "paper" in game_choice or "scissors" in game_choice or "scissor" in game_choice:
            self.rock_paper_scissors()
        elif "online" in game_choice:
            self.play_online_game()
        else:
            self.speech.speak("I didn't recognize that game. Let's play Rock Paper Scissors.")
            self.rock_paper_scissors()
    
    def rock_paper_scissors(self):
        """Play Rock Paper Scissors with GUI"""
        self.speech.speak("Let's play Rock Paper Scissors!")
        
        # Set up the game
        self.player_score = 0
        self.computer_score = 0
        self.max_rounds = 3
        self.current_round = 1
        
        # Create the GUI
        self.create_rps_gui()
    
    def create_rps_gui(self):
        """Create a GUI for Rock Paper Scissors game"""
        # Create main window
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f0f0")
        
        # Create game title
        title_label = Label(self.root, text="Rock Paper Scissors", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)
        
        # Create score display
        self.score_label = Label(self.root, text=f"Player: {self.player_score}  Computer: {self.computer_score}", 
                                font=("Arial", 12), bg="#f0f0f0")
        self.score_label.pack(pady=5)
        
        # Create round display
        self.round_label = Label(self.root, text=f"Round {self.current_round} of {self.max_rounds}", 
                                font=("Arial", 12), bg="#f0f0f0")
        self.round_label.pack(pady=5)
        
        # Create result display
        self.result_label = Label(self.root, text="Choose your move!", font=("Arial", 12), bg="#f0f0f0")
        self.result_label.pack(pady=10)
        
        # Create choices display
        self.player_choice_label = Label(self.root, text="Your choice: ", font=("Arial", 12), bg="#f0f0f0")
        self.player_choice_label.pack()
        
        self.computer_choice_label = Label(self.root, text="Computer's choice: ", font=("Arial", 12), bg="#f0f0f0")
        self.computer_choice_label.pack(pady=5)
        
        # Create buttons frame
        button_frame = Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Create choice buttons
        rock_button = Button(button_frame, text="Rock", width=10, height=2, 
                            command=lambda: self.play_round("rock"))
        rock_button.grid(row=0, column=0, padx=5)
        
        paper_button = Button(button_frame, text="Paper", width=10, height=2, 
                             command=lambda: self.play_round("paper"))
        paper_button.grid(row=0, column=1, padx=5)
        
        scissors_button = Button(button_frame, text="Scissors", width=10, height=2, 
                                command=lambda: self.play_round("scissors"))
        scissors_button.grid(row=0, column=2, padx=5)
        
        # Create new game button
        self.new_game_button = Button(self.root, text="New Game", width=15, height=2, 
                                     command=self.reset_game)
        self.new_game_button.pack(pady=10)
        
        # Start the game
        self.root.mainloop()
    
    def play_round(self, player_choice):
        """Play a round of Rock Paper Scissors"""
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)
        
        # Update choice labels
        self.player_choice_label.config(text=f"Your choice: {player_choice.capitalize()}")
        self.computer_choice_label.config(text=f"Computer's choice: {computer_choice.capitalize()}")
        
        # Determine the winner
        result = self.determine_winner(player_choice, computer_choice)
        
        # Update the score
        if result == "win":
            self.player_score += 1
            self.result_label.config(text="You win this round!")
        elif result == "lose":
            self.computer_score += 1
            self.result_label.config(text="Computer wins this round!")
        else:
            self.result_label.config(text="It's a tie!")
        
        # Update score label
        self.score_label.config(text=f"Player: {self.player_score}  Computer: {self.computer_score}")
        
        # Check if the game is over
        if self.current_round >= self.max_rounds:
            self.end_game()
        else:
            # Move to the next round
            self.current_round += 1
            self.round_label.config(text=f"Round {self.current_round} of {self.max_rounds}")
    
    def determine_winner(self, player_choice, computer_choice):
        """Determine the winner of a round"""
        if player_choice == computer_choice:
            return "tie"
        
        if (player_choice == "rock" and computer_choice == "scissors") or \
           (player_choice == "paper" and computer_choice == "rock") or \
           (player_choice == "scissors" and computer_choice == "paper"):
            return "win"
        else:
            return "lose"
    
    def end_game(self):
        """End the Rock Paper Scissors game"""
        if self.player_score > self.computer_score:
            message = "Congratulations! You win the game!"
        elif self.player_score < self.computer_score:
            message = "Computer wins the game! Better luck next time!"
        else:
            message = "The game is a tie!"
        
        self.result_label.config(text=message)
        messagebox.showinfo("Game Over", message)
    
    def reset_game(self):
        """Reset the Rock Paper Scissors game"""
        self.player_score = 0
        self.computer_score = 0
        self.current_round = 1
        
        # Update labels
        self.score_label.config(text=f"Player: {self.player_score}  Computer: {self.computer_score}")
        self.round_label.config(text=f"Round {self.current_round} of {self.max_rounds}")
        self.result_label.config(text="Choose your move!")
        self.player_choice_label.config(text="Your choice: ")
        self.computer_choice_label.config(text="Computer's choice: ")
    
    def play_online_game(self):
        """Open an online game in the browser"""
        self.speech.speak("Here are some online games I can open for you:")
        
        # List available games
        for i, game in enumerate(self.online_games.keys(), 1):
            self.speech.speak(f"{i}. {game}")
        
        # Get user choice
        self.speech.speak("Which game would you like to play? Please say the number or name.")
        game_choice = input("Choose a game: ").lower()  # For simplicity, using input() instead of speech recognition
        
        # Process the choice
        selected_game = None
        
        # Try to match by number
        if game_choice.isdigit():
            index = int(game_choice) - 1
            if 0 <= index < len(self.online_games):
                selected_game = list(self.online_games.keys())[index]
        
        # Try to match by name
        if not selected_game:
            for game in self.online_games:
                if game.lower() in game_choice:
                    selected_game = game
                    break
        
        # Open the selected game or default to the first one
        if not selected_game:
            self.speech.speak("I couldn't understand your choice. Opening Tic Tac Toe by default.")
            selected_game = list(self.online_games.keys())[0]
        
        self.speech.speak(f"Opening {selected_game}. Enjoy your game!")
        webbrowser.open(self.online_games[selected_game])
