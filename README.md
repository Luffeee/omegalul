# 3D Cube Visualization with ESP32 and WebSocket

## Overview

This project demonstrates a real-time 3D visualization using an ESP32 microcontroller and a Python server with WebSocket communication. The ESP32 reads distance measurements from an ultrasonic sensor and sends this data to a Python server. The server then adjusts the position of a 3D cube in a Pygame window based on these measurements. This creates an interactive 3D visualization that responds to real-world distance changes detected by the ultrasonic sensor.

## Features

- **Real-time Data Communication**: Uses WebSockets for real-time data transmission between the ESP32 and the Python server.
- **3D Visualization**: Implements a 3D rendering of a cube using Pygame and OpenGL, which dynamically adjusts based on sensor data.
- **Ultrasonic Sensor Integration**: Utilizes an ultrasonic sensor connected to the ESP32 to measure distances.

## Hardware Requirements

- ESP32 microcontroller
- Ultrasonic Sensor (HC-SR04)
- Breadboard and jumper wires

## Software Requirements

- Python
- Pygame
- PyOpenGL
- websockets

## Setup and Configuration

### ESP32 and Ultrasonic Sensor

1. **Connect the Ultrasonic Sensor**: Connect the sensor's VCC to 5V on the ESP32, GND to GND, Trig to pin 18, and Echo to pin 19.
2. **Load the ESP32 Code**: Upload the provided code to the ESP32.

### Python WebSocket Server and 3D Visualization

1. **Install Python Dependencies**:
   ```bash
   pip install pygame PyOpenGL websockets
   ```
