#!/usr/bin/env python3
"""
Alert System Module
Sends notifications via Twilio SMS/WhatsApp with threat snapshots
"""

import cv2
import os
import time
import numpy as np
from datetime import datetime
from typing import List, Tuple, Optional

class AlertSystem:
    def __init__(self):
        self.twilio_client = None
        self.alert_history = []
        self.max_alerts_per_hour = 10
        self.alert_cooldown = 30  # seconds
        
        # Try to initialize Twilio
        self.init_twilio()
    
    def init_twilio(self):
        """Initialize Twilio client with fallback to demo mode"""
        try:
            from twilio.rest import Client
            from twilio.base.exceptions import TwilioException
            
            # These would be set as environment variables in production
            # PLACEHOLDER: Insert your Twilio credentials here or set as environment variables
            account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_ACCOUNT_SID')  # PLACEHOLDER
            auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'YOUR_TWILIO_AUTH_TOKEN')    # PLACEHOLDER
            from_number = os.getenv('TWILIO_FROM_NUMBER', '+1234567890')             # PLACEHOLDER
            to_number = os.getenv('TWILIO_TO_NUMBER', '+0987654321')                 # PLACEHOLDER
            
            if all([account_sid, auth_token, from_number, to_number]):
                self.twilio_client = Client(account_sid, auth_token)
                self.from_number = from_number
                self.to_number = to_number
                print("Twilio client initialized successfully!")
            else:
                print("Twilio credentials not found - running in DEMO MODE")
                print("Set environment variables: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, etc.")
                self.twilio_client = None
                
        except ImportError:
            print("Twilio not installed - running in DEMO MODE")
            print("Install with: pip install twilio")
            self.twilio_client = None
        except Exception as e:
            print(f"Error initializing Twilio: {e}")
            print("Falling back to DEMO MODE")
            self.twilio_client = None
    
    def send_alert(self, frame: np.ndarray, threats: List[str], boxes: List[Tuple[int, int, int, int]]):
        """
        Send alert with threat information and snapshot
        Args:
            frame: Current video frame
            threats: List of detected threats
            boxes: List of threat bounding boxes
        """
        current_time = time.time()
        
        # Check rate limiting
        if not self._can_send_alert(current_time):
            return
        
        # Create alert message
        message = self._create_alert_message(threats)
        
        # Save snapshot
        snapshot_path = self._save_snapshot(frame, threats, boxes)
        
        # Send alert
        if self.twilio_client:
            self._send_twilio_alert(message, snapshot_path)
        else:
            self._send_demo_alert(message, snapshot_path)
        
        # Record alert
        self.alert_history.append({
            'timestamp': current_time,
            'threats': threats,
            'message': message,
            'snapshot': snapshot_path
        })
        
        print(f"🚨 ALERT SENT: {message}")
    
    def _can_send_alert(self, current_time: float) -> bool:
        """Check if we can send an alert (rate limiting)"""
        # Remove old alerts (older than 1 hour)
        self.alert_history = [
            alert for alert in self.alert_history 
            if current_time - alert['timestamp'] < 3600
        ]
        
        # Check hourly limit
        if len(self.alert_history) >= self.max_alerts_per_hour:
            return False
        
        # Check cooldown period
        if self.alert_history:
            last_alert_time = self.alert_history[-1]['timestamp']
            if current_time - last_alert_time < self.alert_cooldown:
                return False
        
        return True
    
    def _create_alert_message(self, threats: List[str]) -> str:
        """Create alert message from threat list"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if len(threats) == 1:
            threat_text = threats[0]
        else:
            threat_text = ", ".join(threats[:-1]) + f" and {threats[-1]}"
        
        message = f"🚨 SECURITY ALERT 🚨\n"
        message += f"Time: {timestamp}\n"
        message += f"Threat Detected: {threat_text}\n"
        message += f"Location: Surveillance Camera 1\n"
        message += f"Action Required: Immediate attention needed"
        
        return message
    
    def _save_snapshot(self, frame: np.ndarray, threats: List[str], 
                      boxes: List[Tuple[int, int, int, int]]) -> str:
        """Save threat snapshot with annotations"""
        # Create snapshots directory if it doesn't exist
        os.makedirs('snapshots', exist_ok=True)
        
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshots/threat_{timestamp}.jpg"
        
        # Draw threat annotations on snapshot
        snapshot = frame.copy()
        for i, (threat, box) in enumerate(zip(threats, boxes)):
            x1, y1, x2, y2 = box
            
            # Draw bounding box
            color = (0, 0, 255) if threat == "person" else (0, 165, 255)
            cv2.rectangle(snapshot, (x1, y1), (x2, y2), color, 3)
            
            # Draw label
            label = f"{threat.upper()}"
            cv2.putText(snapshot, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Add timestamp to image
        cv2.putText(snapshot, timestamp, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Save image
        cv2.imwrite(filename, snapshot)
        return filename
    
    def _send_twilio_alert(self, message: str, snapshot_path: str):
        """Send alert via Twilio SMS/WhatsApp"""
        try:
            # Send text message
            self.twilio_client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            # TODO: Send image via MMS (requires different Twilio endpoint)
            # For demo purposes, we'll just send the text message
            
        except Exception as e:
            print(f"Error sending Twilio alert: {e}")
            # Fallback to demo mode
            self._send_demo_alert(message, snapshot_path)
    
    def _send_demo_alert(self, message: str, snapshot_path: str):
        """Demo alert - simulates sending notification"""
        print("\n" + "="*50)
        print("📱 DEMO ALERT SIMULATION")
        print("="*50)
        print(f"To: +1234567890")
        print(f"From: +1987654321")
        print(f"Message: {message}")
        print(f"Snapshot: {snapshot_path}")
        print("="*50)
        print("In production, this would be sent via Twilio SMS/WhatsApp")
        print("="*50 + "\n")
    
    def get_alert_summary(self) -> dict:
        """Get summary of recent alerts"""
        current_time = time.time()
        recent_alerts = [
            alert for alert in self.alert_history 
            if current_time - alert['timestamp'] < 3600  # Last hour
        ]
        
        threat_counts = {}
        for alert in recent_alerts:
            for threat in alert['threats']:
                threat_counts[threat] = threat_counts.get(threat, 0) + 1
        
        return {
            'total_alerts': len(recent_alerts),
            'threat_breakdown': threat_counts,
            'last_alert': recent_alerts[-1]['timestamp'] if recent_alerts else None
        } 