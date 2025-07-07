#!/usr/bin/env python3
"""
Demo Script for AI Surveillance MVP
Showcases system capabilities with interactive demonstrations
"""

import cv2
import numpy as np
import time    
from datetime import datetime
from main import SurveillancePipeline

class SurveillanceDemo:
    def __init__(self):
        self.pipeline = SurveillancePipeline()
        self.demo_scenarios = [
            "normal_operation",
            "after_hours_intrusion", 
            "fire_detection",
            "privacy_protection"
        ]
        self.current_scenario = 0
        self.scenario_duration = 15  # seconds per scenario
        
    def run_demo(self):
        """Run the complete demo sequence"""
        print("\n" + "="*60)
        print("🚨 AI SURVEILLANCE MVP - DEMO MODE")
        print("="*60)
        print("This demo showcases the system's capabilities:")
        print("• Real-time threat detection")
        print("• Privacy protection with face blurring")
        print("• After-hours intrusion detection")
        print("• Alert system with snapshots")
        print("="*60)
        
        # Show configuration
        self.pipeline.config.print_status()
        
        print("\n🎮 Demo Controls:")
        print("• Press 'n' to cycle through scenarios")
        print("• Press 'a' to toggle after-hours mode")
        print("• Press 'q' to quit demo")
        print("• Press 's' to show scenario info")
        
        # Start demo loop
        self._run_demo_loop()
    
    def _run_demo_loop(self):
        """Main demo loop with scenario cycling"""
        cap = cv2.VideoCapture(0)  # Use webcam
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        scenario_start_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error reading from webcam")
                    break
                
                # Check if it's time to cycle scenarios
                current_time = time.time()
                if current_time - scenario_start_time > self.scenario_duration:
                    self._next_scenario()
                    scenario_start_time = current_time
                
                # Process frame with current scenario
                processed_frame = self._process_demo_frame(frame)
                
                # Display result
                cv2.imshow('AI Surveillance MVP - Demo Mode', processed_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('n'):
                    self._next_scenario()
                    scenario_start_time = current_time
                elif key == ord('a'):
                    self.pipeline.config.toggle_after_hours()
                elif key == ord('s'):
                    self._show_scenario_info()
                
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("\nDemo completed!")
    
    def _process_demo_frame(self, frame):
        """Process frame with demo-specific enhancements"""
        # Apply current scenario effects
        frame = self._apply_scenario_effects(frame)
        
        # Run normal pipeline processing
        processed_frame = self.pipeline.process_frame(frame)
        
        # Add demo-specific overlay
        processed_frame = self._add_demo_overlay(processed_frame)
        
        return processed_frame
    
    def _apply_scenario_effects(self, frame):
        """Apply visual effects based on current scenario"""
        scenario = self.demo_scenarios[self.current_scenario]
        
        if scenario == "after_hours_intrusion":
            # Force after-hours mode
            self.pipeline.config.after_hours_enabled = True
            # Add dark overlay to simulate night
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
            
        elif scenario == "fire_detection":
            # Add orange tint to simulate fire lighting
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 100, 255), -1)
            cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
            
        elif scenario == "privacy_protection":
            # Add privacy notice overlay
            cv2.putText(frame, "PRIVACY MODE ACTIVE", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
    
    def _add_demo_overlay(self, frame):
        """Add demo-specific information overlay"""
        height, width = frame.shape[:2]
        
        # Scenario info overlay
        scenario = self.demo_scenarios[self.current_scenario]
        scenario_name = scenario.replace('_', ' ').title()
        
        # Background for scenario info
        overlay = frame.copy()
        cv2.rectangle(overlay, (width - 300, 10), (width - 10, 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Scenario text
        cv2.putText(frame, f"DEMO SCENARIO:", (width - 290, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, scenario_name, (width - 290, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Demo controls reminder
        cv2.putText(frame, "Press 'n' for next scenario", (10, height - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Press 'a' to toggle after-hours", (10, height - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Press 'q' to quit", (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def _next_scenario(self):
        """Cycle to next demo scenario"""
        self.current_scenario = (self.current_scenario + 1) % len(self.demo_scenarios)
        scenario = self.demo_scenarios[self.current_scenario]
        scenario_name = scenario.replace('_', ' ').title()
        
        print(f"\n🔄 Switching to scenario: {scenario_name}")
        self._show_scenario_info()
    
    def _show_scenario_info(self):
        """Display information about current scenario"""
        scenario = self.demo_scenarios[self.current_scenario]
        
        print("\n" + "="*50)
        print(f"📋 CURRENT SCENARIO: {scenario.replace('_', ' ').title()}")
        print("="*50)
        
        if scenario == "normal_operation":
            print("• Standard surveillance mode")
            print("• Detecting people, objects, and threats")
            print("• Face blurring for privacy")
            print("• Normal alert thresholds")
            
        elif scenario == "after_hours_intrusion":
            print("• After-hours mode (10 PM - 6 AM)")
            print("• Person detection = HIGH PRIORITY")
            print("• Red bounding boxes for intrusions")
            print("• Immediate alerts for any movement")
            
        elif scenario == "fire_detection":
            print("• Fire/smoke detection priority")
            print("• Orange bounding boxes for fire/smoke")
            print("• Highest priority alerts")
            print("• Emergency response simulation")
            
        elif scenario == "privacy_protection":
            print("• Enhanced privacy mode")
            print("• All non-threat faces blurred")
            print("• Privacy notice overlay")
            print("• Demonstrates ethical AI usage")
        
        print("="*50)

def main():
    """Run the surveillance demo"""
    demo = SurveillanceDemo()
    demo.run_demo()

if __name__ == "__main__":
    main() 