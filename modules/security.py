#!/usr/bin/env python3
# Security Module - Face Recognition

import os
import cv2
import numpy as np
import time

class FaceSecurity:
    def __init__(self):
        # Create directories if they don't exist
        self.face_data_dir = os.path.join("assets", "face_data")
        os.makedirs(self.face_data_dir, exist_ok=True)
        
        # Load face cascade for detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Load face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Try to load existing face model if available
        self.model_path = os.path.join(self.face_data_dir, "face_model.yml")
        try:
            self.recognizer.read(self.model_path)
            self.model_exists = True
            print("Face recognition model loaded successfully")
        except:
            self.model_exists = False
            print("No face recognition model found")
    
    def capture_face(self):
        """Capture a face from the webcam"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return None
        
        print("Capturing face... Please look at the camera")
        
        # Warmup the camera
        for _ in range(5):
            ret, frame = cap.read()
            time.sleep(0.1)
        
        # Capture the face
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture frame")
            cap.release()
            return None
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            print("No face detected")
            cap.release()
            return None
        
        # Get the largest face
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        # Extract face region
        face_img = gray[y:y+h, x:x+w]
        
        # Release the webcam
        cap.release()
        
        return face_img
    
    def train_face_model(self):
        """Train the face recognition model"""
        print("Starting face recognition training...")
        
        # Capture multiple face samples
        face_samples = []
        for i in range(5):
            print(f"Capturing sample {i+1}/5...")
            face = self.capture_face()
            if face is not None:
                face_samples.append(face)
            time.sleep(1)
        
        if len(face_samples) < 3:
            print("Not enough samples captured")
            return False
        
        # Train the model
        print("Training face recognition model...")
        face_arrays = [np.array(face, 'uint8') for face in face_samples]
        face_labels = [0] * len(face_arrays)  # Label 0 for the authorized user
        
        self.recognizer.train(face_arrays, np.array(face_labels))
        self.recognizer.save(self.model_path)
        self.model_exists = True
        
        print("Face recognition model trained successfully")
        return True
    
    def authenticate_face(self):
        """Authenticate using face recognition"""
        if not self.model_exists:
            print("No face model exists. Please train the model first.")
            return self.train_face_model()
        
        # Capture a face
        face = self.capture_face()
        if face is None:
            print("Could not capture a face for authentication")
            return False
        
        # Predict
        label, confidence = self.recognizer.predict(face)
        
        # Check if the face is recognized (lower confidence is better)
        if label == 0 and confidence < 70:  # Threshold can be adjusted
            print(f"Authentication successful (confidence: {confidence})")
            return True
        else:
            print(f"Authentication failed (confidence: {confidence})")
            return False
