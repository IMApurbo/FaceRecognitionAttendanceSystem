import cv2
import face_recognition
import os
import csv
from datetime import datetime

# Path to the folder containing known faces
KNOWN_FACES_DIR = 'known_faces'

# Initialize some variables
known_face_encodings = []
known_face_names = []

# Load known faces
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Load the image file
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        # Encode the face
        face_encoding = face_recognition.face_encodings(image)[0]
        # Get the name from the filename
        name = os.path.splitext(filename)[0]
        # Append the encoding and name to the lists
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

# Open a CSV file to store attendance records
with open('attendance.csv', 'a', newline='') as csvfile:
    fieldnames = ['Name', 'Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Initialize webcam
    video_capture = cv2.VideoCapture(1)

    while True:
        # Capture a single frame of video
        ret, frame = video_capture.read()

        # Find all the faces and face encodings in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Log attendance
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow({'Name': name, 'Time': current_time})

            # Draw a box around the face
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
