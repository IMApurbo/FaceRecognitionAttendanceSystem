import cv2
import os
import json
import face_recognition

# Directory to save user images
USER_IMAGES_DIR = 'user_images'
USER_JSON_FILE = os.path.join(USER_IMAGES_DIR, 'users.json')

if not os.path.exists(USER_IMAGES_DIR):
    os.makedirs(USER_IMAGES_DIR)

# Load or create the JSON file to store user data
if os.path.exists(USER_JSON_FILE):
    with open(USER_JSON_FILE, 'r') as f:
        users_data = json.load(f)
else:
    users_data = {}

def get_next_photo_number(user_name):
    """ Get the next available photo number for the user """
    if user_name in users_data:
        existing_numbers = [
            int(filename.split('_')[-1].split('.')[0])
            for filename in users_data[user_name]
            if filename.split('_')[-1].split('.')[0].isdigit()
        ]
        if existing_numbers:
            return max(existing_numbers) + 1
    return 1

def capture_photo(user_name, actual_name):
    cap = cv2.VideoCapture(1)
    face_detected = False

    while not face_detected:
        ret, frame = cap.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            face_detected = True
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected! Taking photo in 3 seconds...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Register', frame)
            cv2.waitKey(1000)

            for i in range(3, 0, -1):
                ret, frame = cap.read()
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"Taking photo in {i}...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Register', frame)
                cv2.waitKey(1000)

            ret, clean_frame = cap.read()
            photo_number = get_next_photo_number(user_name)
            save_path = os.path.join(USER_IMAGES_DIR, f"{actual_name.replace(' ', '_').lower()}_{photo_number}.jpg")
            cv2.imwrite(save_path, clean_frame)
            print(f"Photo saved as {save_path}")

            if user_name in users_data:
                users_data[user_name].append(f"{actual_name.replace(' ', '_').lower()}_{photo_number}.jpg")
            else:
                users_data[user_name] = [f"{actual_name.replace(' ', '_').lower()}_{photo_number}.jpg"]

            with open(USER_JSON_FILE, 'w') as f:
                json.dump(users_data, f, indent=4)
            break

        cv2.imshow('Register', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def register_new_user():
    actual_name = input("Enter the actual name of the new user: ")
    if actual_name:
        user_name = actual_name
        capture_photo(user_name, actual_name)

def select_existing_user():
    if not users_data:
        print("No users found!")
        return

    print("Select User:")
    for i, user in enumerate(users_data.keys(), 1):
        print(f"{i}. {user}")

    try:
        choice = int(input("Enter the number of the user: "))
        if 1 <= choice <= len(users_data):
            selected_user = list(users_data.keys())[choice - 1]
            user_action(selected_user)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def user_action(user_name):
    print(f"Selected User: {user_name}")
    print("1. Add More Photos")
    print("2. Delete Account")
    print("3. Go Back")

    choice = input("Enter your choice: ")
    if choice == '1':
        capture_photo(user_name, user_name)
    elif choice == '2':
        delete_user_account(user_name)
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please try again.")

def delete_user_account(user_name):
    confirm = input(f"Are you sure you want to delete {user_name} and all their photos? (yes/no): ")
    if confirm.lower() == 'yes':
        for filename in users_data[user_name]:
            os.remove(os.path.join(USER_IMAGES_DIR, filename))
        del users_data[user_name]
        with open(USER_JSON_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)
        print(f"User {user_name} and their photos have been deleted.")

def main():
    while True:
        print("Face Recognition System")
        print("1. Register New User")
        print("2. Existing User")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            register_new_user()
        elif choice == '2':
            select_existing_user()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
