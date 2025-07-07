#!/usr/bin/env python3
"""
Test Script for AI Surveillance MVP
Verifies all components are working correctly
"""

import sys
import os
import cv2
import numpy as np

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError:
        print("❌ OpenCV import failed")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError:
        print("❌ NumPy import failed")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics imported successfully")
    except ImportError:
        print("⚠️  Ultralytics not available - will run in demo mode")
    
    try:
        from twilio.rest import Client
        print("✅ Twilio imported successfully")
    except ImportError:
        print("⚠️  Twilio not available - will run in demo mode")
    
    return True

def test_opencv():
    """Test OpenCV functionality"""
    print("\n🔍 Testing OpenCV...")
    
    try:
        # Test camera access
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera access successful")
            ret, frame = cap.read()
            if ret:
                print(f"✅ Frame captured: {frame.shape}")
            else:
                print("❌ Frame capture failed")
            cap.release()
        else:
            print("⚠️  Camera not available - will need video file for testing")
        
        # Test face cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        if not face_cascade.empty():
            print("✅ Face detection model loaded")
        else:
            print("❌ Face detection model failed to load")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenCV test failed: {e}")
        return False

def test_components():
    """Test individual components"""
    print("\n🔍 Testing components...")
    
    try:
        from detector import ThreatDetector
        detector = ThreatDetector()
        print("✅ Threat detector initialized")
        
        from blur_faces import FaceBlurrer
        blurrer = FaceBlurrer()
        print("✅ Face blurrer initialized")
        
        from alert import AlertSystem
        alert_system = AlertSystem()
        print("✅ Alert system initialized")
        
        from config import Config
        config = Config()
        print("✅ Configuration loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

def test_pipeline():
    """Test the main pipeline"""
    print("\n🔍 Testing pipeline...")
    
    try:
        from main import SurveillancePipeline
        pipeline = SurveillancePipeline()
        print("✅ Surveillance pipeline initialized")
        
        # Test with a dummy frame
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        processed_frame = pipeline.process_frame(dummy_frame)
        print("✅ Pipeline processing successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚨 AI SURVEILLANCE MVP - SYSTEM TEST")
    print("="*50)
    
    tests = [
        ("Imports", test_imports),
        ("OpenCV", test_opencv),
        ("Components", test_components),
        ("Pipeline", test_pipeline)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "="*50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\nTo start the surveillance system:")
        print("  python main.py")
        print("\nTo run the interactive demo:")
        print("  python demo.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("  pip install -r requirements.txt")
        print("  Check camera permissions")
        print("  Ensure all dependencies are installed")
    
    print("="*50)

if __name__ == "__main__":
    main() 