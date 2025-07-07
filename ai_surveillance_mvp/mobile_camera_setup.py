#!/usr/bin/env python3
"""
Mobile Camera Setup for AI Surveillance MVP
Multiple ways to use mobile phone as camera input
"""

import cv2
import requests
import numpy as np
from urllib.parse import urlparse
import time

class MobileCameraSetup:
    def __init__(self):
        self.camera_url = None
        self.camera_type = None
        
    def setup_ip_camera(self, app_name="IP Webcam"):
        """Setup instructions for IP camera apps"""
        print("\n" + "="*60)
        print("📱 MOBILE CAMERA SETUP - IP CAMERA APPS")
        print("="*60)
        
        if app_name.lower() == "ip webcam":
            print("1. Install 'IP Webcam' app on your phone")
            print("2. Open the app and tap 'Start server'")
            print("3. Note the IP address shown (e.g., 192.168.1.100:8080)")
            print("4. The video stream URL will be:")
            print("   http://[IP]:8080/video")
            print("5. Enter the URL when prompted")
            
        elif app_name.lower() == "droidcam":
            print("1. Install 'DroidCam' on your phone")
            print("2. Install 'DroidCam Client' on your computer")
            print("3. Connect both devices to same WiFi")
            print("4. Use the IP address shown in DroidCam app")
            
        elif app_name.lower() == "epocam":
            print("1. Install 'EpocCam' on your phone")
            print("2. Install 'EpocCam Driver' on your computer")
            print("3. Connect both devices to same WiFi")
            print("4. EpocCam will appear as a webcam device")
        
        print("="*60)
        
    def test_camera_url(self, url):
        """Test if a camera URL is accessible"""
        try:
            print(f"Testing camera URL: {url}")
            cap = cv2.VideoCapture(url)
            
            if not cap.isOpened():
                print("❌ Could not open camera URL")
                return False
            
            ret, frame = cap.read()
            if not ret:
                print("❌ Could not read frame from camera")
                return False
            
            print(f"✅ Camera working! Frame size: {frame.shape}")
            cap.release()
            return True
            
        except Exception as e:
            print(f"❌ Error testing camera: {e}")
            return False
    
    def get_common_ip_camera_urls(self):
        """Get common IP camera URL patterns"""
        return {
            "IP Webcam": "http://[IP]:8080/video",
            "DroidCam": "http://[IP]:4747/video",
            "Epocam": "http://[IP]:4747/video",
            "ManyCam": "http://[IP]:8080/video",
            "Custom": "http://[IP]:[PORT]/video"
        }
    
    def setup_mobile_camera(self):
        """Interactive setup for mobile camera"""
        print("\n📱 MOBILE CAMERA SETUP")
        print("="*40)
        
        print("Choose your mobile camera method:")
        print("1. IP Camera App (IP Webcam, DroidCam, etc.)")
        print("2. USB Connection (Android ADB)")
        print("3. WiFi Direct")
        print("4. Manual URL input")
        print("5. Show setup instructions")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            self._setup_ip_camera_app()
        elif choice == "2":
            self._setup_usb_connection()
        elif choice == "3":
            self._setup_wifi_direct()
        elif choice == "4":
            self._setup_manual_url()
        elif choice == "5":
            self._show_all_instructions()
        else:
            print("❌ Invalid choice")
    
    def _setup_ip_camera_app(self):
        """Setup IP camera app"""
        print("\n📱 IP CAMERA APP SETUP")
        print("="*30)
        
        apps = ["IP Webcam", "DroidCam", "Epocam", "ManyCam"]
        print("Available apps:")
        for i, app in enumerate(apps, 1):
            print(f"{i}. {app}")
        
        app_choice = input("\nChoose app (1-4): ").strip()
        
        if app_choice in ["1", "2", "3", "4"]:
            app_name = apps[int(app_choice) - 1]
            self.setup_ip_camera(app_name)
            
            # Get IP address
            ip = input("\nEnter your phone's IP address: ").strip()
            if ip:
                # Common ports for different apps
                ports = {
                    "IP Webcam": "8080",
                    "DroidCam": "4747", 
                    "Epocam": "4747",
                    "ManyCam": "8080"
                }
                port = ports.get(app_name, "8080")
                url = f"http://{ip}:{port}/video"
                
                print(f"\nTesting URL: {url}")
                if self.test_camera_url(url):
                    self.camera_url = url
                    self.camera_type = "ip_camera"
                    print("✅ Mobile camera setup successful!")
                    self._save_config()
                else:
                    print("❌ Camera test failed. Check your setup.")
    
    def _setup_usb_connection(self):
        """Setup USB connection via ADB"""
        print("\n🔌 USB CONNECTION SETUP")
        print("="*30)
        print("1. Enable Developer Options on your Android phone")
        print("2. Enable USB Debugging")
        print("3. Connect phone via USB")
        print("4. Install ADB on your computer")
        print("5. Run: adb forward tcp:8080 tcp:8080")
        print("6. Use URL: http://localhost:8080/video")
        
        # This would require ADB setup which is more complex
        print("\n⚠️  USB setup requires ADB installation")
        print("For easier setup, use IP camera apps instead")
    
    def _setup_wifi_direct(self):
        """Setup WiFi Direct connection"""
        print("\n📶 WIFI DIRECT SETUP")
        print("="*30)
        print("1. Enable WiFi Direct on both devices")
        print("2. Connect phone to computer via WiFi Direct")
        print("3. Use IP camera app with direct connection")
        print("4. Use the IP address provided by WiFi Direct")
        
        ip = input("\nEnter WiFi Direct IP address: ").strip()
        if ip:
            url = f"http://{ip}:8080/video"
            if self.test_camera_url(url):
                self.camera_url = url
                self.camera_type = "wifi_direct"
                print("✅ WiFi Direct setup successful!")
                self._save_config()
    
    def _setup_manual_url(self):
        """Setup with manual URL input"""
        print("\n🔗 MANUAL URL SETUP")
        print("="*30)
        
        url = input("Enter camera stream URL: ").strip()
        if url:
            if self.test_camera_url(url):
                self.camera_url = url
                self.camera_type = "manual"
                print("✅ Manual URL setup successful!")
                self._save_config()
            else:
                print("❌ URL test failed")
    
    def _show_all_instructions(self):
        """Show all setup instructions"""
        print("\n📚 COMPLETE SETUP INSTRUCTIONS")
        print("="*50)
        
        print("\n1️⃣ IP WEBCAM (Android)")
        self.setup_ip_camera("IP Webcam")
        
        print("\n2️⃣ DROIDCAM (Android/iOS)")
        self.setup_ip_camera("DroidCam")
        
        print("\n3️⃣ EPOCAM (iOS)")
        self.setup_ip_camera("Epocam")
        
        print("\n4️⃣ USB CONNECTION")
        print("• Install ADB tools")
        print("• Enable USB debugging")
        print("• Run: adb forward tcp:8080 tcp:8080")
        print("• Use: http://localhost:8080/video")
        
        print("\n5️⃣ WIFI DIRECT")
        print("• Enable WiFi Direct on both devices")
        print("• Connect directly")
        print("• Use IP camera app")
        
        print("\n6️⃣ BLUETOOTH (Limited)")
        print("• Some apps support Bluetooth")
        print("• Lower quality but no WiFi needed")
    
    def _save_config(self):
        """Save camera configuration"""
        if self.camera_url:
            config_content = f"""# Mobile Camera Configuration
CAMERA_URL = "{self.camera_url}"
CAMERA_TYPE = "{self.camera_type}"
"""
            
            with open("mobile_camera_config.py", "w") as f:
                f.write(config_content)
            
            print(f"\n✅ Configuration saved to mobile_camera_config.py")
            print(f"Camera URL: {self.camera_url}")
    
    def run_with_mobile_camera(self):
        """Run surveillance system with mobile camera"""
        if not self.camera_url:
            print("❌ No mobile camera configured")
            print("Run setup first: python mobile_camera_setup.py")
            return
        
        print(f"\n🚀 Starting surveillance with mobile camera...")
        print(f"Camera URL: {self.camera_url}")
        
        try:
            from main import SurveillancePipeline
            pipeline = SurveillancePipeline()
            pipeline.run(self.camera_url)
        except Exception as e:
            print(f"❌ Error running with mobile camera: {e}")

def main():
    """Main function"""
    setup = MobileCameraSetup()
    
    print("📱 MOBILE CAMERA SETUP FOR AI SURVEILLANCE")
    print("="*50)
    
    # Check if config exists
    try:
        import mobile_camera_config
        print("✅ Mobile camera configuration found!")
        setup.camera_url = mobile_camera_config.CAMERA_URL
        setup.camera_type = mobile_camera_config.CAMERA_TYPE
        
        choice = input("Run surveillance with mobile camera? (y/n): ").strip().lower()
        if choice == 'y':
            setup.run_with_mobile_camera()
        else:
            setup.setup_mobile_camera()
    except ImportError:
        print("No mobile camera configuration found.")
        setup.setup_mobile_camera()

if __name__ == "__main__":
    main() 