#!/usr/bin/env python3
"""
Configuration Module
Centralized settings for the AI Surveillance MVP
"""

import os
from datetime import datetime, time

class Config:
    def __init__(self):
        # Demo Mode Settings
        self.demo_mode = True
        self.after_hours_enabled = True
        
        # Time Settings
        self.restricted_start_hour = 22  # 10 PM
        self.restricted_end_hour = 6    # 6 AM
        
        # Detection Settings
        self.confidence_threshold = 0.5
        self.detection_interval = 1  # Process every N frames
        
        # Alert Settings
        self.alert_cooldown = 30  # seconds between alerts
        self.max_alerts_per_hour = 10
        
        # Privacy Settings
        self.blur_strength = 15
        self.blur_non_threat_faces = True
        
        # Video Settings
        self.frame_width = 640
        self.frame_height = 480
        self.fps = 30
        
        # File Paths
        self.snapshots_dir = "snapshots"
        self.logs_dir = "logs"
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.snapshots_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def is_after_hours(self) -> bool:
        """Check if current time is during restricted hours"""
        if not self.after_hours_enabled:
            return False
        
        current_time = datetime.now().time()
        start_time = time(self.restricted_start_hour, 0)
        end_time = time(self.restricted_end_hour, 0)
        
        # Handle overnight restriction (e.g., 10 PM to 6 AM)
        if self.restricted_start_hour > self.restricted_end_hour:
            return current_time >= start_time or current_time <= end_time
        else:
            return start_time <= current_time <= end_time
    
    def toggle_after_hours(self):
        """Toggle after-hours mode on/off"""
        self.after_hours_enabled = not self.after_hours_enabled
        status = "ON" if self.after_hours_enabled else "OFF"
        print(f"After Hours Mode: {status}")
    
    def get_threat_priority(self, threat_type: str) -> int:
        """Get priority level for different threat types"""
        priority_map = {
            "fire": 1,      # Highest priority
            "smoke": 1,     # Highest priority
            "person": 2,    # Medium priority (depends on time)
            "backpack": 3,  # Lower priority
            "handbag": 3,   # Lower priority
            "suitcase": 3   # Lower priority
        }
        return priority_map.get(threat_type, 4)  # Default lowest priority
    
    def should_alert(self, threat_type: str) -> bool:
        """Determine if a threat should trigger an alert"""
        priority = self.get_threat_priority(threat_type)
        
        # Always alert for high priority threats
        if priority == 1:
            return True
        
        # Alert for person during after hours
        if threat_type == "person" and self.is_after_hours():
            return True
        
        # For demo mode, alert for medium priority threats too
        if self.demo_mode and priority <= 2:
            return True
        
        return False
    
    def get_demo_settings(self) -> dict:
        """Get demo-specific settings"""
        return {
            "demo_mode": self.demo_mode,
            "after_hours_enabled": self.after_hours_enabled,
            "restricted_hours": f"{self.restricted_start_hour}:00 - {self.restricted_end_hour}:00",
            "current_time": datetime.now().strftime("%H:%M:%S"),
            "is_after_hours": self.is_after_hours()
        }
    
    def print_status(self):
        """Print current configuration status"""
        print("\n" + "="*40)
        print("AI SURVEILLANCE MVP - CONFIGURATION")
        print("="*40)
        print(f"Demo Mode: {'ON' if self.demo_mode else 'OFF'}")
        print(f"After Hours Mode: {'ON' if self.after_hours_enabled else 'OFF'}")
        print(f"Restricted Hours: {self.restricted_start_hour}:00 - {self.restricted_end_hour}:00")
        print(f"Current Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Is After Hours: {'YES' if self.is_after_hours() else 'NO'}")
        print(f"Confidence Threshold: {self.confidence_threshold}")
        print(f"Alert Cooldown: {self.alert_cooldown}s")
        print(f"Max Alerts/Hour: {self.max_alerts_per_hour}")
        print("="*40) 