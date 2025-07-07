#!/usr/bin/env python3
"""
Threat Detection Module
Uses YOLOv8 for real-time object detection with fallback demo logic
"""

import cv2
import numpy as np
import time
from typing import List, Tuple, Optional

class ThreatDetector:
    def __init__(self, model_path: str = 'yolov8m.pt', confidence_threshold: float = 0.5, class_thresholds: Optional[dict] = None):
        """
        Args:
            model_path (str): Path to YOLOv8 model (default: yolov8m.pt for better accuracy)
            confidence_threshold (float): Default detection confidence threshold
            class_thresholds (dict): Optional per-class confidence thresholds
        """
        self.model = None
        self.current_threats = []
        self.confidence_threshold = confidence_threshold
        self.class_thresholds = class_thresholds or {}
        self.target_classes = ['person', 'fire', 'smoke', 'backpack', 'handbag', 'suitcase']
        self.model_path = model_path
        
        # Try to load YOLOv8 model, fallback to demo mode
        self.load_model()
    
    def load_model(self):
        """Load YOLOv8 model with fallback to demo mode"""
        try:
            from ultralytics import YOLO
            print(f"Loading YOLOv8 model from {self.model_path} ...")
            self.model = YOLO(self.model_path)
            print("YOLOv8 model loaded successfully!")
        except ImportError:
            print("Ultralytics not available - running in DEMO MODE")
            print("Install with: pip install ultralytics")
            self.model = None
        except Exception as e:
            print(f"Error loading YOLOv8 model: {e}")
            print("Falling back to DEMO MODE")
            self.model = None
    
    def detect(self, frame: np.ndarray) -> Tuple[List[str], List[Tuple[int, int, int, int]], List[float]]:
        """
        Detect threats in the frame
        Returns: (threat_types, bounding_boxes, confidence_scores)
        """
        if self.model is not None:
            return self._detect_with_yolo(frame)
        else:
            return self._detect_demo(frame)
    
    def _detect_with_yolo(self, frame: np.ndarray) -> Tuple[List[str], List[Tuple[int, int, int, int]], List[float]]:
        """Real YOLOv8 detection with per-class threshold support"""
        results = self.model(frame, verbose=False)
        
        threats = []
        boxes = []
        scores = []
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = result.names[class_id]
                    # Use per-class threshold if available
                    threshold = self.class_thresholds.get(class_name, self.confidence_threshold)
                    if confidence < threshold:
                        continue
                    if class_name in self.target_classes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        threats.append(class_name)
                        boxes.append((x1, y1, x2, y2))
                        scores.append(confidence)
        
        self.current_threats = threats
        return threats, boxes, scores
    
    def _detect_demo(self, frame: np.ndarray) -> Tuple[List[str], List[Tuple[int, int, int, int]], List[float]]:
        """Demo detection - simulates detection for presentation purposes"""
        threats = []
        boxes = []
        scores = []
        
        height, width = frame.shape[:2]
        current_time = time.time()
        
        # Simulate periodic detections for demo
        demo_cycle = int(current_time) % 10  # Changes every 10 seconds
        
        if demo_cycle < 3:
            # Simulate person detection
            x1, y1, x2, y2 = width//4, height//4, width//2, height//2
            threats.append("person")
            boxes.append((x1, y1, x2, y2))
            scores.append(0.85)
            
        elif demo_cycle < 6:
            # Simulate fire detection
            x1, y1, x2, y2 = width//3, height//3, 2*width//3, 2*height//3
            threats.append("fire")
            boxes.append((x1, y1, x2, y2))
            scores.append(0.92)
            
        elif demo_cycle < 9:
            # Simulate smoke detection
            x1, y1, x2, y2 = width//6, height//6, 5*width//6, 5*height//6
            threats.append("smoke")
            boxes.append((x1, y1, x2, y2))
            scores.append(0.78)
        
        # Add some random noise for realism
        if np.random.random() < 0.1:  # 10% chance
            x1 = np.random.randint(0, width//2)
            y1 = np.random.randint(0, height//2)
            x2 = x1 + np.random.randint(50, 150)
            y2 = y1 + np.random.randint(50, 150)
            
            threat_types = ["backpack", "handbag", "suitcase"]
            threat = np.random.choice(threat_types)
            
            threats.append(threat)
            boxes.append((x1, y1, x2, y2))
            scores.append(np.random.uniform(0.6, 0.9))
        
        self.current_threats = threats
        return threats, boxes, scores
    
    def get_threat_summary(self) -> dict:
        """Get summary of current threats"""
        threat_counts = {}
        for threat in self.current_threats:
            threat_counts[threat] = threat_counts.get(threat, 0) + 1
        return threat_counts 