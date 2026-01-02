# Virtual Painter using OpenCV & MediaPipe Hands

A real-time **Virtual Painter** application that lets you draw on the screen using hand gestures. Built with **Python**, **OpenCV**, and **MediaPipe**, it detects hand landmarks to distinguish between **selection mode** (choose colors or tools) and **drawing mode**.  

---

## Features

- Real-time hand tracking using **MediaPipe**  
- Finger-based gesture controls for **drawing** and **tool selection**  
- Multiple **brush colors** and **eraser**  
- Persistent **canvas** with live video feed  
- Customizable toolbar for **color/tool selection**  
- Supports **1080p resolution** for high-quality drawing  

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/virtual-painter.git
cd virtual-painter

---
2.Install required dependencies:
pip install opencv-python mediapipe numpy

3.Run the main Python script:
python virtual_painter.py
