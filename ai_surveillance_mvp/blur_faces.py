#!/usr/bin/env python3
"""
Face Blurring Module for Privacy Protection
Blurs faces of non-threat individuals while keeping threats visible
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional

class FaceBlurrer:
    def __init__(self):
        self.face_cascade = None
        self.blur_strength = 15
        self.load_face_detector()
    
    def load_face_detector(self):
        """Load face detection model with fallback"""
        try:
            # Try to load OpenCV's Haar Cascade for face detection
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                print("Warning: Could not load face cascade - running without face blurring")
                self.face_cascade = None
            else:
                print("Face detection model loaded successfully!")
                
        except Exception as e:
            print(f"Error loading face detector: {e}")
            print("Running without face blurring")
            self.face_cascade = None
    
    def blur_faces(self, frame: np.ndarray, threats: List[str], threat_boxes: List[Tuple[int, int, int, int]]) -> np.ndarray:
        """
        Blur faces in the frame, except for those in threat areas
        Args:
            frame: Input frame
            threats: List of detected threat types
            threat_boxes: List of threat bounding boxes
        Returns:
            Frame with faces blurred
        """
        if self.face_cascade is None:
            return frame
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Create a copy of the frame for blurring
        blurred_frame = frame.copy()
        
        for (x, y, w, h) in faces:
            # Check if this face is in a threat area
            if not self._is_face_in_threat_area(x, y, w, h, threat_boxes, threats):
                # Blur this face
                face_roi = blurred_frame[y:y+h, x:x+w]
                blurred_face = self._apply_blur(face_roi)
                blurred_frame[y:y+h, x:x+w] = blurred_face
        
        return blurred_frame
    
    def _is_face_in_threat_area(self, face_x: int, face_y: int, face_w: int, face_h: int, 
                               threat_boxes: List[Tuple[int, int, int, int]], 
                               threats: List[str]) -> bool:
        """
        Check if a face overlaps with any threat area
        Returns True if face should NOT be blurred (it's a threat)
        """
        face_center_x = face_x + face_w // 2
        face_center_y = face_y + face_h // 2
        
        for i, (threat_x1, threat_y1, threat_x2, threat_y2) in enumerate(threat_boxes):
            # Only consider person threats for face blurring logic
            if threats[i] == "person":
                # Check if face center is within threat box
                if (threat_x1 <= face_center_x <= threat_x2 and 
                    threat_y1 <= face_center_y <= threat_y2):
                    return True
        
        return False
    
    def _apply_blur(self, roi: np.ndarray) -> np.ndarray:
        """Apply Gaussian blur to a region of interest"""
        # Apply strong Gaussian blur
        blurred = cv2.GaussianBlur(roi, (self.blur_strength, self.blur_strength), 0)
        return blurred
    
    def demo_blur_faces(self, frame: np.ndarray) -> np.ndarray:
        """Demo version - simulates face blurring for presentation"""
        height, width = frame.shape[:2]
        
        # Create demo face regions to blur
        demo_faces = [
            (width//6, height//6, 80, 80),
            (3*width//4, height//4, 60, 60),
            (width//2, 3*height//4, 70, 70)
        ]
        
        blurred_frame = frame.copy()
        
        for (x, y, w, h) in demo_faces:
            # Ensure coordinates are within frame bounds
            x = max(0, min(x, width - w))
            y = max(0, min(y, height - h))
            
            face_roi = blurred_frame[y:y+h, x:x+w]
            blurred_face = cv2.GaussianBlur(face_roi, (25, 25), 0)
            blurred_frame[y:y+h, x:x+w] = blurred_face
        
        return blurred_frame 