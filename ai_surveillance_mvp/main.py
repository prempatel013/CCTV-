#!/usr/bin/env python3
"""
AI-Powered Surveillance MVP - Main Pipeline
Real-time threat detection with privacy protection and alert system
"""

import cv2
import time
import numpy as np
from datetime import datetime
from detector import ThreatDetector     
from blur_faces import FaceBlurrer
from alert import AlertSystem
from config import Config 

class SurveillancePipeline:
    def __init__(self):
        self.config = Config()
        self.detector = ThreatDetector()
        self.face_blurrer = FaceBlurrer()
        self.alert_system = AlertSystem()
        self.frame_count = 0
        self.last_alert_time = 0
        
    def process_frame(self, frame):
        """Process a single frame through the surveillance pipeline"""
        self.frame_count += 1
        
        # Step 1: Detect threats
        threats, boxes, scores = self.detector.detect(frame)
        
        # Step 2: Blur non-threat faces for privacy
        processed_frame = self.face_blurrer.blur_faces(frame, threats, boxes)
        
        # Step 3: Draw detection results
        processed_frame = self.draw_detections(processed_frame, threats, boxes, scores)
        
        # Step 4: Check for alerts
        self.check_alerts(frame, threats, boxes)
        
        return processed_frame
    
    def draw_detections(self, frame, threats, boxes, scores):
        """Draw bounding boxes and labels on the frame"""
        for i, (threat, box, score) in enumerate(zip(threats, boxes, scores)):
            x1, y1, x2, y2 = box
            label = f"{threat}: {score:.2f}"
            
            # Color coding based on threat type
            if threat == "person" and self.config.is_after_hours():
                color = (0, 0, 255)  # Red for after-hours intrusion
            elif threat in ["fire", "smoke"]:
                color = (0, 165, 255)  # Orange for fire/smoke
            else:
                color = (0, 255, 0)  # Green for other detections
            
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label background
            (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - label_height - 10), (x1 + label_width, y1), color, -1)
            
            # Draw label text
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add status overlay
        self.draw_status_overlay(frame)
        
        return frame
    
    def draw_status_overlay(self, frame):
        """Draw status information overlay"""
        height, width = frame.shape[:2]
        
        # Status background
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Status text
        status_text = [
            f"AI Surveillance MVP - Demo Mode",
            f"Frame: {self.frame_count}",
            f"Time: {datetime.now().strftime('%H:%M:%S')}",
            f"After Hours: {'ON' if self.config.is_after_hours() else 'OFF'}",
            f"Threats Detected: {len(self.detector.current_threats)}"
        ]
        
        for i, text in enumerate(status_text):
            y_pos = 30 + i * 20
            cv2.putText(frame, text, (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def check_alerts(self, frame, threats, boxes):
        """Check if alerts should be triggered"""
        current_time = time.time()
        
        # Prevent spam alerts (minimum 30 seconds between alerts)
        if current_time - self.last_alert_time < 30:
            return
        
        # Check for high-priority threats
        high_priority_threats = []
        for threat in threats:
            if threat in ["fire", "smoke"] or (threat == "person" and self.config.is_after_hours()):
                high_priority_threats.append(threat)
        
        if high_priority_threats:
            self.alert_system.send_alert(frame, high_priority_threats, boxes)
            self.last_alert_time = current_time
    
    def run(self, video_source=0):
        """Main pipeline execution loop"""
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print("Error: Could not open video source")
            return
        
        print("AI Surveillance MVP Started")
        print("Press 'q' to quit, 'a' to toggle after-hours mode")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("End of video stream")
                    break
                
                # Process frame through pipeline
                processed_frame = self.process_frame(frame)
                
                # Display result
                cv2.imshow('AI Surveillance MVP - Demo', processed_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('a'):
                    self.config.toggle_after_hours()
                    print(f"After Hours Mode: {'ON' if self.config.is_after_hours() else 'OFF'}")
                
        except KeyboardInterrupt:
            print("\nStopping surveillance pipeline...")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Surveillance pipeline stopped")

def main():
    """Entry point for the surveillance system"""
    pipeline = SurveillancePipeline()
    
    # Check for mobile camera configuration
    try:
        import mobile_camera_config
        print(f"📱 Using mobile camera: {mobile_camera_config.CAMERA_URL}")
        pipeline.run(mobile_camera_config.CAMERA_URL)
    except ImportError:
        # For demo: use webcam (0) or specify video file path
        # Example: pipeline.run("demo_video.mp4")
        print("📹 Using webcam (press 'm' for mobile camera setup)")
        pipeline.run(0)

if __name__ == "__main__":
    main() 