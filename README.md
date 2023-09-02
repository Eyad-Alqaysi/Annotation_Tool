
# Annotation_Tool for Gate Counting

## Introduction

The Annotation_Tool is designed to assist in preparing test data for YOLO (You Only Look Once) models by annotating video frames. This tool simplifies the task of marking entering and leaving points in a video sequence, thereby aiding in the development and testing of gate counting applications.

## Features

- **User-friendly Interface**: Utilizes Tkinter for a simple and intuitive UI.
- **Point Annotations**: Allows the user to mark entering and leaving points on a video frame.
- **Pause and Resume**: Offers the ability to pause and resume the video for accurate annotations.
- **JSON Support**: Save and load annotations in JSON format.
- **Customization**: Ability to adjust video speed and dimensions.

## Requirements

- Python 3.x
- Tkinter
- OpenCV (`cv2`)
- PIL (Pillow)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Eyad-Alqaysi/Annotation_Tool.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Annotation_Tool
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the tool:
    ```bash
    python main.py
    ```
2. Use the "Upload" button to load a video.
3. Press the "Space" key to start or pause the video.
4. Right-click to add a leaving point and left-click to add an entering point. Use the middle-click to delete the last point.
5. Save the points and counts in a JSON file using the "Save" button.
6. Load saved points from a JSON file using the "Load" button.
7. Reset the annotations by using the "Reset" button.