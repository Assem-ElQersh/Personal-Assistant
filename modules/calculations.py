#!/usr/bin/env python3
# Calculations Module - Math operations

import math
import re

class Calculator:
    def __init__(self):
        # Import speech engine here to avoid circular imports
        from modules.speech_engine import SpeechEngine
        self.speech = SpeechEngine()
    
    def evaluate_expression(self, expression):
        """Safely evaluate a mathematical expression"""
        # Replace words with symbols
        expression = expression.lower().replace('plus', '+').replace('minus', '-')
        expression = expression.replace('times', '*').replace('multiplied by', '*')
        expression = expression.replace('divided by', '/').replace('over', '/')
        expression = expression.replace('power', '**').replace('to the power of', '**')
        
        # Remove any characters that aren't digits, operators, or decimals
        expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        
        # Remove extra spaces
        expression = expression.replace(' ', '')
        
        try:
            # Evaluate the expression
            result = eval(expression)
            return result
        except:
            return None
    
    def factorial(self, n):
        """Calculate the factorial of a number"""
        try:
            n = int(n)
            if n < 0:
                return None
            return math.factorial(n)
        except:
            return None
    
    def binary(self, n):
        """Convert a number to binary"""
        try:
            n = int(n)
            return bin(n)[2:]  # Remove the '0b' prefix
        except:
            return None
    
    def process_calculation(self, command):
        """Process various math calculations based on the command"""
        command = command.lower()
        result = None
        
        # Basic arithmetic
        if any(op in command for op in ['plus', 'minus', 'times', 'divided by', 'multiplied by']):
            # Extract the expression from the command
            expression = command.replace("calculate", "").replace("what is", "").strip()
            result = self.evaluate_expression(expression)
            
            if result is not None:
                self.speech.speak(f"The result is {result}")
            else:
                self.speech.speak("I couldn't calculate that. Please try again.")
        
        # Factorial
        elif "factorial" in command:
            match = re.search(r'factorial\s+(\d+)', command)
            if not match:
                match = re.search(r'factorial\s+of\s+(\d+)', command)
            
            if match:
                n = int(match.group(1))
                result = self.factorial(n)
                if result is not None:
                    self.speech.speak(f"The factorial of {n} is {result}")
                else:
                    self.speech.speak("I couldn't calculate that factorial.")
            else:
                self.speech.speak("Please specify a number for the factorial calculation.")
        
        # Binary conversion
        elif "binary" in command:
            match = re.search(r'binary\s+of\s+(\d+)', command)
            if not match:
                match = re.search(r'binary\s+(\d+)', command)
            
            if match:
                n = int(match.group(1))
                result = self.binary(n)
                if result is not None:
                    self.speech.speak(f"The binary representation of {n} is {result}")
                else:
                    self.speech.speak("I couldn't convert that number to binary.")
            else:
                self.speech.speak("Please specify a number for the binary conversion.")
        
        # Trigonometric functions
        elif any(func in command for func in ["sin", "cos", "tan"]):
            # Sine
            if "sin" in command:
                match = re.search(r'sin\s+(\d+)', command)
                if match:
                    angle = int(match.group(1))
                    # Convert to radians if in degrees
                    if "degree" in command or "degrees" in command:
                        angle_rad = math.radians(angle)
                    else:
                        angle_rad = angle
                    
                    result = math.sin(angle_rad)
                    self.speech.speak(f"The sine of {angle} {'degrees' if 'degree' in command else 'radians'} is {result:.4f}")
            
            # Cosine
            elif "cos" in command:
                match = re.search(r'cos\s+(\d+)', command)
                if match:
                    angle = int(match.group(1))
                    # Convert to radians if in degrees
                    if "degree" in command or "degrees" in command:
                        angle_rad = math.radians(angle)
                    else:
                        angle_rad = angle
                    
                    result = math.cos(angle_rad)
                    self.speech.speak(f"The cosine of {angle} {'degrees' if 'degree' in command else 'radians'} is {result:.4f}")
            
            # Tangent
            elif "tan" in command:
                match = re.search(r'tan\s+(\d+)', command)
                if match:
                    angle = int(match.group(1))
                    # Convert to radians if in degrees
                    if "degree" in command or "degrees" in command:
                        angle_rad = math.radians(angle)
                    else:
                        angle_rad = angle
                    
                    result = math.tan(angle_rad)
                    self.speech.speak(f"The tangent of {angle} {'degrees' if 'degree' in command else 'radians'} is {result:.4f}")
        
        # Logarithm
        elif "log" in command:
            match = re.search(r'log\s+of\s+(\d+)', command)
            if not match:
                match = re.search(r'log\s+(\d+)', command)
            
            if match:
                n = float(match.group(1))
                if "base" in command:
                    base_match = re.search(r'base\s+(\d+)', command)
                    if base_match:
                        base = float(base_match.group(1))
                        result = math.log(n, base)
                        self.speech.speak(f"The logarithm of {n} with base {base} is {result:.4f}")
                else:
                    result = math.log10(n)
                    self.speech.speak(f"The logarithm (base 10) of {n} is {result:.4f}")
            else:
                self.speech.speak("Please specify a number for the logarithm calculation.")
        
        # Square root
        elif "square root" in command:
            match = re.search(r'square\s+root\s+of\s+(\d+)', command)
            if not match:
                match = re.search(r'square\s+root\s+(\d+)', command)
            
            if match:
                n = float(match.group(1))
                result = math.sqrt(n)
                self.speech.speak(f"The square root of {n} is {result:.4f}")
            else:
                self.speech.speak("Please specify a number for the square root calculation.")
        
        # Bit shifting
        elif "shift" in command:
            # Right shift
            if "right shift" in command:
                match = re.search(r'right\s+shift\s+(\d+)', command)
                if match:
                    n = int(match.group(1))
                    positions = 1  # Default
                    pos_match = re.search(r'by\s+(\d+)', command)
                    if pos_match:
                        positions = int(pos_match.group(1))
                    
                    result = n >> positions
                    self.speech.speak(f"{n} right-shifted by {positions} is {result}")
            
            # Left shift
            elif "left shift" in command:
                match = re.search(r'left\s+shift\s+(\d+)', command)
                if match:
                    n = int(match.group(1))
                    positions = 1  # Default
                    pos_match = re.search(r'by\s+(\d+)', command)
                    if pos_match:
                        positions = int(pos_match.group(1))
                    
                    result = n << positions
                    self.speech.speak(f"{n} left-shifted by {positions} is {result}")
        
        # If no specific calculation was detected
        else:
            self.speech.speak("I couldn't understand what calculation you want me to perform.")
