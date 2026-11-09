# HandWall – AI Virtual Handwriting System

A computer vision project that allows users to write virtually using hand gestures and a laptop camera.

## Project Overview

HandWall uses Python, OpenCV, and MediaPipe to detect hand movements and create smooth, neon-style handwriting on the screen.

Users can write words using their thumb and index finger, release the gesture to move to another position, and clear the canvas when needed.

## Features

- Real-time hand tracking
- Gesture-controlled virtual writing
- Smooth finger movement
- Neon handwriting effect
- Multiple words and separate writing strokes
- Clear canvas functionality
- Uses a built-in webcam

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

## Requirements

- Python 3.12
- Laptop with a webcam
- macOS, Windows, or Linux

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd HandWall
```

Create a virtual environment:

```bash
python3.12 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python main.py
```

## Controls

| Gesture / Key | Action |
|---|---|
| Pinch thumb and index finger | Write |
| Release pinch | Stop writing |
| C | Clear canvas |
| Q | Quit |

## Future Improvements

- Multiple neon colors
- Gesture-based color selection
- Virtual keyboard
- Handwriting recognition
- Full-screen digital wall interface

## Author

Latasha Nayak

B.Tech Computer Science and Engineering

## License

This project is available under the MIT License.