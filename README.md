# MonSight 👓

### An Agentic AI Navigation & Safety Assistant for Visually Impaired People

MonSight is an AI-powered assistant designed to help visually impaired users
navigate their surroundings more safely and independently.

Instead of only detecting objects, MonSight combines perception, location,
route information, and risk assessment to continuously decide what action
should be taken.

## 🔄 Core Intelligence Loop

PERCEIVE → UNDERSTAND → REASON → DECIDE → ACT → VERIFY → REPEAT

## 🎯 Problem

Visually impaired people may encounter obstacles, vehicles, unfamiliar
locations, and other environmental hazards while moving independently.

Traditional object detection can identify an object, but identifying an
object is not enough. The system must understand its potential risk and
provide an appropriate action.

## 💡 Solution

MonSight combines multiple AI tools:

- 👁️ Vision Tool — detects surrounding objects
- 📍 Location Tool — tracks movement and location
- 🗺️ Map & Route Tool — provides navigation information
- ⚠️ Safety & Risk Tool — evaluates potential hazards
- 💊 Medicine Tool — reads medicine labels using OCR
- 🧠 MonSight Agent — coordinates the tools and determines the response
- 🔊 Voice Guidance — communicates decisions to the user

## ✨ Key Features

### 1. Real-Time Object Detection
Uses YOLO to detect objects through a camera.

### 2. Risk Assessment
Objects are classified according to potential safety risk.

Example:

Car nearby → CRITICAL → STOP

Person nearby → MEDIUM → SLOW DOWN

### 3. Continuous Verification
MonSight checks hazards across multiple camera frames before taking action,
reducing unnecessary alerts.

### 4. Navigation Assistance
Provides route information and walking instructions to destinations.

### 5. Medicine Label Reading
Uses OCR to read medicine names, strength, and expiry information.

MonSight does NOT provide medical dosage or treatment recommendations.

## 🧠 Architecture

User
 ↓
Camera / GPS
 ↓
MonSight Agent
 ↓
┌──────────────┬──────────────┬──────────────┐
│ Vision Tool  │ Location     │ Map & Route  │
│              │ Tool         │ Tool         │
└──────────────┴──────────────┴──────────────┘
 ↓
Safety & Risk Tool
 ↓
Agent Reasoning
 ↓
Decision
 ↓
Voice Guidance
 ↓
Verification
 ↓
Repeat

## 🛠️ Technology Stack

- Python
- OpenCV
- YOLO
- NumPy
- Tesseract OCR
- pyttsx3
- Ultralytics
- Git & GitHub

## 📂 Project Structure

```text
MonSight/
├── main.py
├── realtime_camera.py
├── tools/
│   ├── vision_tool.py
│   ├── location_tool.py
│   ├── map_route_tool.py
│   ├── safety_risk_tool.py
│   ├── monsight_agent.py
│   └── medicine_tool.py
└── tests/
    └── safety_test.py
🚀 Current Prototype

The current prototype demonstrates:

Real-time camera-based object detection
Risk classification
Stable hazard verification
STOP / CAUTION / SLOW DOWN / CONTINUE decisions
Voice alerts
Navigation prototype
Medicine label OCR
🔮 Future Scope
Wearable smart-glasses integration
Real GPS-based navigation
Indoor navigation
Pothole and road-damage detection
Traffic-crossing assistance
Better distance estimation
Emergency assistance
Personalized navigation
⚠️ Safety

MonSight is a research prototype and decision-support system.

It should not be treated as a replacement for human judgment or professional
medical advice.

👩‍💻 Author

Monika-2108

Built as an AI/ML hackathon project.

📜 License

This project is currently intended for educational and research purposes.