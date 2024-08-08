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

# Define a dictionary with person names and corresponding list of filenames
face_names = {
    'Leonel Messi': ['messi.jpg', 'messi2.jpg'],
    'Neymar Jr.': ['neymar.jpg'],
    'Cristiano Ronaldo': ['ronaldo.jpg']
    # Add more names and lists of filenames as needed
}

# Load known faces
for name, filenames in face_names.items():
    for filename in filenames:
        # Load the image file
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        # Encode the face
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            face_encoding = face_encodings[0]
            # Append the encoding and name to the lists
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
        else:
            print(f"Warning: No faces found in {filename}")

# Open a CSV file to store attendance records
with open('attendance.csv', 'a', newline='') as csvfile:
    fieldnames = ['Name', 'Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Initialize webcam
    video_capture = cv2.VideoCapture(1)

    # Set to keep track of logged faces
    logged_faces = set()

    while True:
        # Capture a single frame of video
        ret, frame = video_capture.read()

        # Find all the faces and face encodings in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Check if a match was found in known_face_encodings
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Print the detected name in the terminal
            print(f"Detected: {name}")

            # Log attendance if a known face is detected
            if name != "Unknown" and name not in logged_faces:
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow({'Name': name, 'Time': current_time})
                logged_faces.add(name)
                print(f"Logged {name} at {current_time}")

            # Draw a box around the face
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            fontScale = 0.5  # Adjust this value to change text size
            fontThickness = 1  # Adjust this value to change text thickness
            cv2.putText(frame, name, (left + 6, bottom - 6), font, fontScale, (255, 255, 255), fontThickness)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Clear the logged_faces set periodically if needed, e.g., every minute
        # This is optional, depending on your specific requirements

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
