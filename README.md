# AI-Powered Surveillance MVP 🚨

A real-time intelligent surveillance system using mobile camera footage to simulate CCTV input. Built for hackathon/demo presentations with privacy protection and alert-based notifications.

## 🎯 Core Features

### Real-Time Threat Detection
- **YOLOv8 Integration**: Advanced object detection for people, fire, smoke, and suspicious objects
- **Model Selection**: Easily switch between YOLOv8 variants (nano, small, medium, large) or use custom-trained models
- **Per-Class Thresholds**: Configure detection confidence per class for higher accuracy
- **Demo Mode**: Fallback simulation when YOLOv8 is not available
- **After-Hours Intrusion**: Special detection logic for restricted time periods (10 PM - 6 AM)
- **Advanced Features (Extensible)**: Placeholders for object tracking (e.g., DeepSORT) and zone-based detection

### Privacy Protection
- **Face Blurring**: Automatically blurs faces of non-threat individuals
- **Selective Visibility**: Only threats remain clearly visible in output
- **OpenCV Haar Cascade**: Fast and reliable face detection

### Alert System
- **Twilio Integration**: SMS/WhatsApp notifications with threat snapshots
- **Demo Alerts**: Simulated notifications for presentation purposes
- **Rate Limiting**: Prevents alert spam with configurable cooldowns

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam or video file for input
- (Optional) Twilio account for real alerts

### Installation

1. **Clone and navigate to the project:**
```bash
cd ai_surveillance_mvp
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the surveillance system:**
```bash
python main.py   
```

### Demo Mode
The system automatically runs in demo mode if YOLOv8 or Twilio are not available, making it perfect for presentations and hackathons.

## 📁 Project Structure

```
ai_surveillance_mvp/
├── main.py               # Main pipeline orchestrator
├── detector.py           # YOLOv8 threat detection
├── blur_faces.py         # Privacy protection via face blurring
├── alert.py              # Twilio alert system
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── snapshots/           # Threat snapshots (auto-created)
└── logs/                # System logs (auto-created)
```

## 🎮 Usage

### Basic Operation
1. **Start the system**: `python main.py`
2. **View live feed**: The processed video stream will display
3. **Toggle after-hours mode**: Press `a` to simulate restricted hours
4. **Quit**: Press `q` to exit

### Controls
- `q` - Quit the application
- `a` - Toggle after-hours mode (simulates 10 PM - 6 AM)

### Demo Features
- **Simulated Detections**: Rotating threat types every 10 seconds
- **Face Blurring**: Demo face regions are blurred for privacy
- **Alert Simulation**: Console-based alert notifications
- **Status Overlay**: Real-time system information display

## ⚙️ Configuration

### Environment Variables (Optional)
For real Twilio alerts, set these environment variables:
```bash
export TWILIO_ACCOUNT_SID="your_account_sid"
export TWILIO_AUTH_TOKEN="your_auth_token"
export TWILIO_FROM_NUMBER="+1234567890"
export TWILIO_TO_NUMBER="+0987654321"
```

### Custom Settings
Modify `config.py` to adjust:
- Restricted hours (default: 10 PM - 6 AM)
- Detection confidence threshold
- Alert cooldown periods
- Privacy blur strength

## 🔧 Technical Details

### Detection Model
- **Model Path**: Easily specify which YOLOv8 model to use (e.g., yolov8n.pt, yolov8m.pt, yolov8l.pt, or custom weights)
- **Per-Class Thresholds**: Set different confidence thresholds for each class
- **Extensible**: Codebase is ready for object tracking and zone-based detection integration

### Detection Classes
- **person**: Human detection (high priority during after-hours)
- **fire**: Fire detection (highest priority)
- **smoke**: Smoke detection (highest priority)
- **backpack/handbag/suitcase**: Suspicious objects (lower priority)

### Privacy Logic
- Faces are detected using OpenCV Haar Cascade
- Non-threat faces are blurred with Gaussian blur
- Threat faces remain visible for security purposes
- Blur strength is configurable

### Alert System
- **Rate Limiting**: Maximum 10 alerts per hour
- **Cooldown**: 30 seconds between alerts
- **Snapshots**: Threat images saved with annotations
- **Fallback**: Demo mode when Twilio unavailable

## 🎯 Demo Scenarios

### 1. After-Hours Intrusion
- Toggle after-hours mode with `a`
- Person detection becomes high-priority threat
- Red bounding boxes indicate intrusion alerts

### 2. Fire/Smoke Detection
- Orange bounding boxes for fire/smoke
- Immediate alert triggers
- Highest priority notifications

### 3. Privacy Protection
- Non-threat faces are automatically blurred
- Threat faces remain visible
- Demonstrates privacy-first approach

## 🛠️ Development

### Adding New Threat Types & Advanced Features
1. Update `target_classes` and `class_thresholds` in `detector.py`
2. Add priority mapping in `config.py`
3. Update alert logic as needed
4. (Optional) Integrate object tracking or zone-based detection in `main.py`

### Custom Video Sources
```python
# Use video file
pipeline.run("path/to/video.mp4")

# Use IP camera
pipeline.run("rtsp://camera_ip:port/stream")

# Use specific webcam
pipeline.run(1)  # Second camera
```

### Performance Optimization
- Use `yolov8n.pt` for speed (nano model)
- Adjust `detection_interval` in config
- Reduce frame resolution for faster processing

### Upgrading Detection
- Change the model path in `main.py` or `detector.py` to use a more accurate YOLOv8 model
- Set per-class thresholds for fine-grained control
- Add or remove target classes as needed
- Integrate tracking or zone logic in the pipeline (see TODOs in `main.py`)

## 🚨 Alert Examples

### Demo Alert Output
```
==================================================
📱 DEMO ALERT SIMULATION
==================================================
To: +1234567890
From: +1987654321
Message: 🚨 SECURITY ALERT 🚨
Time: 2024-01-15 22:30:45
Threat Detected: person
Location: Surveillance Camera 1
Action Required: Immediate attention needed
Snapshot: snapshots/threat_20240115_223045.jpg
==================================================
In production, this would be sent via Twilio SMS/WhatsApp
==================================================
```

## 🔒 Privacy & Ethics

This MVP is designed for:
- **Educational purposes** and hackathon demonstrations
- **Privacy-first approach** with automatic face blurring
- **Ethical AI usage** with clear threat classification
- **Demo environments** only - not for production surveillance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes only.

## 🆘 Troubleshooting

### Common Issues

**"No module named 'ultralytics'"**
```bash
pip install ultralytics
```

**"No module named 'cv2'"**
```bash
pip install opencv-python
```

**Webcam not working**
- Check camera permissions
- Try different camera index: `pipeline.run(1)`
- Use video file instead: `pipeline.run("demo.mp4")`

**Performance issues**
- Reduce frame resolution in `config.py`
- Use smaller YOLO model
- Increase `detection_interval`

**Model not accurate enough**
- Use a larger YOLOv8 model (e.g., yolov8m.pt or yolov8l.pt)
- Adjust per-class thresholds in `main.py` or `detector.py`

---

**Built for Hackathons & Demos** 🚀
*Showcase AI-powered surveillance with privacy protection and real-time alerts!* 