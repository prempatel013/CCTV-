#!/usr/bin/env python3
"""
Quick Start Script for AI Surveillance MVP
Automatically sets up and runs the surveillance system
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install core dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"])
        print("✅ Core dependencies installed")
        
        # Try to install optional dependencies
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
            print("✅ YOLOv8 installed - full detection mode available")
        except:
            print("⚠️  YOLOv8 not installed - will run in demo mode")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "twilio"])
            print("✅ Twilio installed - real alerts available")
        except:
            print("⚠️  Twilio not installed - will run in demo mode")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_tests():
    """Run system tests"""
    print("\n🔍 Running system tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_menu():
    """Show main menu"""
    print("\n" + "="*50)
    print("🚨 AI SURVEILLANCE MVP - QUICK START")
    print("="*50)
    print("Choose an option:")
    print("1. Run basic surveillance system")
    print("2. Run interactive demo")
    print("3. Run system tests")
    print("4. Show configuration")
    print("5. Exit")
    print("="*50)

def run_surveillance():
    """Run the main surveillance system"""
    print("\n🚀 Starting surveillance system...")
    print("Press 'q' to quit, 'a' to toggle after-hours mode")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nSurveillance stopped by user")
    except Exception as e:
        print(f"❌ Error running surveillance: {e}")

def run_demo():
    """Run the interactive demo"""
    print("\n🎮 Starting interactive demo...")
    print("Press 'n' to cycle scenarios, 'a' to toggle after-hours, 'q' to quit")
    
    try:
        subprocess.run([sys.executable, "demo.py"])
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def show_config():
    """Show current configuration"""
    try:
        from config import Config
        config = Config()
        config.print_status()
    except Exception as e:
        print(f"❌ Error loading config: {e}")

def main():
    """Main quick start function"""
    print("🚨 AI SURVEILLANCE MVP - QUICK START")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but continuing...")
    
    # Main menu loop
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                run_surveillance()
            elif choice == "2":
                run_demo()
            elif choice == "3":
                run_tests()
            elif choice == "4":
                show_config()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 