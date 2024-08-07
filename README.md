```markdown
# Face Recognition Attendance System

This project is a Face Recognition Attendance System built using Python, OpenCV, and the `face_recognition` library. The system recognizes faces from a live video feed and logs attendance in a CSV file.

## Features

- Real-time face detection and recognition
- Attendance logging in a CSV file
- Easy to add new known faces
- Visual feedback with bounding boxes and labels

## Requirements

- Python 3.x
- OpenCV
- face_recognition
- numpy

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/IMApurbo/FaceRecognitionAttendanceSystem.git
   cd FaceRecognitionAttendanceSystem
   ```

2. **Install the required packages:**
   ```bash
   pip install opencv-python face_recognition numpy
   ```

3. **Create a folder named `known_faces`** in the project directory and add images of known persons. Name the images with the person's name (e.g., `john_doe.jpg`).

## Usage

1. **Run the script:**
   ```bash
   python attendance_system.py
   ```

2. The webcam will open, and the system will start recognizing faces from the `known_faces` folder and log attendance in `attendance.csv`.

## Code Explanation

### Loading Known Faces

The script loads images from the `known_faces` folder, encodes the faces, and stores the encodings and names in lists.

```python
import os
import face_recognition

KNOWN_FACES_DIR = 'known_faces'
known_face_encodings = []
known_face_names = []

for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        name = os.path.splitext(filename)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)
```

### Real-Time Face Recognition and Attendance Logging

The script captures video from the webcam, recognizes faces, and logs attendance in a CSV file.

```python
import cv2
import csv
from datetime import datetime

with open('attendance.csv', 'a', newline='') as csvfile:
    fieldnames = ['Name', 'Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow({'Name': name, 'Time': current_time})

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Python](https://www.python.org/)

```
