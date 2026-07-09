<p align="center">
  <img src="./demo-assets/banner.png" alt="AI Gesture Mouse Control Banner" width="100%">
</p>

<h1 align="center">Gesture Mouse Control</h1>

<p align="center">
Touchless Desktop Interaction using Computer Vision
</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/>

<img src="https://img.shields.io/badge/MediaPipe-FF6F00?style=for-the-badge"/>

<img src="https://img.shields.io/badge/PyAutoGUI-2C2C2C?style=for-the-badge"/>

</p>

<p align="center">

<b>Move • Click • Swipe • Control</b>

</p>

<p align="center">

Control your computer using nothing but your hand gestures.
Built with <b>MediaPipe</b>, <b>OpenCV</b>, and <b>PyAutoGUI</b> for smooth, real-time desktop interaction.

</p>

---

## 📖 Overview

Traditional mouse devices require physical interaction. This project demonstrates how computer vision and hand tracking can provide a natural, touch-free alternative.

Using Google's **MediaPipe Hands**, the application continuously detects both hands, identifies finger states, and maps different gestures to desktop actions.

The project focuses on low-latency interaction, smooth cursor movement, and intuitive gesture controls while maintaining real-time performance.

---

## 🎥 Demo

<p align="center">
<img src="./demo-assets/demo.gif" width="95%">
</p>

<p align="center">
<i>Real-time cursor movement, click gestures, and swipe navigation.</i>
</p>

## ✨ Features

- 🖱️ Smooth real-time cursor movement
- ✊ Cursor freeze using a closed fist
- 🤏 Pinch gesture for left mouse click
- 👉 Swipe left and right gestures
- 🎯 Custom control zone mapping
- ⚡ Cursor smoothing algorithm
- 📈 Real-time FPS display
- 🤖 Dual-hand gesture recognition
- 🎥 Live webcam tracking

---

## 🖐 Supported Gestures

| Gesture | Action |
|----------|--------|
| ☝ Index Finger | Cursor Movement |
| ✊ Closed Fist | Pause Cursor |
| 🤏 Thumb + Index Pinch | Left Click |
| ✌ Index + Middle Swipe Right | Right Arrow Key |
| ✌ Index + Middle Swipe Left | Left Arrow Key |

---

## ⚙ How It Works

```
Webcam
      │
      ▼
OpenCV Video Capture
      │
      ▼
MediaPipe Hands
      │
      ▼
Hand Landmark Detection
      │
      ▼
Gesture Recognition
      │
      ▼
Cursor Mapping
      │
      ▼
PyAutoGUI
      │
      ▼
Operating System
```

---

## 🏗 System Architecture

### Hand Detection

The webcam continuously captures video frames.

Each frame is processed using **MediaPipe Hands**, producing 21 landmarks for every detected hand.

The application distinguishes between the **left** and **right** hand, allowing different gestures to trigger different actions.

---

### Cursor Control

The **right hand** controls cursor movement.

The index fingertip position is mapped from the webcam's control zone to the monitor's full resolution using interpolation.

To reduce cursor jitter, a smoothing algorithm gradually moves the cursor toward the target position instead of jumping directly.

---

### Gesture Recognition

The **left hand** is responsible for command gestures.

Implemented gestures include:

- Pinch detection for mouse clicks
- Swipe detection for keyboard navigation
- Finger state recognition
- Closed fist detection to freeze cursor movement

---

### Performance Optimizations

Several optimizations were implemented to improve responsiveness and reduce latency.

- Lightweight MediaPipe model
- Cursor smoothing
- Reduced detection complexity
- Optimized tracking confidence
- Control zone mapping
- Experimental frame-skipping support

---

## ⚙ Tech Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Hand Tracking | MediaPipe |
| Mouse Control | PyAutoGUI |
| Mathematics | NumPy + Math |
| Webcam Interface | OpenCV |

---

## 🚀
