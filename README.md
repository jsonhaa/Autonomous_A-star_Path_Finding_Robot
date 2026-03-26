# Autonomous A* Pathfinding Robot

A wireless autonomous robot that uses the A* pathfinding 
algorithm to navigate a grid, communicating between a 
Python script and an ESP32 microcontroller over WiFi.

## Overview
This project combines pathfinding algorithms with embedded 
systems to create a robot that can autonomously navigate 
from a start position to a goal while avoiding obstacles.

The system consists of two main components:
- **Python (Laptop)** — Runs A* algorithm, generates 
  optimal path, converts path to motor commands and sends 
  them wirelessly to the robot
- **C++ (ESP32)** — Receives commands over WiFi and 
  controls motors to physically navigate the grid

## How It Works
1. A* algorithm finds optimal path on a grid map
2. Path is converted to physical commands (F, L, R)
3. Commands sent wirelessly via WiFi TCP socket
4. ESP32 receives commands and drives motors accordingly
5. Robot navigates from start to goal

## Hardware
- ESP32 microcontroller
- L298N dual motor driver
- 2x DC motors
- 3x AA batteries (ESP32 power)
- 9V battery (motor power)

## Software
- Python 3 (pathfinding + communication)
- Arduino IDE / C++ (ESP32 firmware)

## Communication
- Protocol: WiFi TCP Socket
- Port: 8080
- Commands: F (forward), R (turn right), L (turn left)
- Responses: OK (success), BLOCKED (obstacle detected)

## Algorithm
A* uses Manhattan distance heuristic to find the optimal 
path. The grid supports configurable maps with obstacles, 
start and goal positions. Path is converted to physical 
robot commands accounting for robot orientation.

## Setup
### Python
```bash
pip install socket
python Astar.py
```

### ESP32
1. Open Arduino IDE
2. Install ESP32 board package
3. Update WiFi credentials in code
4. Upload to ESP32

## Project Structure
```
├── Astar.py          # Python A* implementation + WiFi communication
├── esp32_robot.ino   # ESP32 motor control + WiFi server
└── README.md
```

## Future Improvements
- Add ultrasonic sensors for real time obstacle detection
- Implement dynamic replanning when obstacles detected
- Add camera for position feedback
- Expand to larger grid sizes


