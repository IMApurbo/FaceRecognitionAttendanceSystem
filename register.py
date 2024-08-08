import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import cv2
import os
import time
import face_recognition
import json

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
        # Extract the numbers from existing photos
        existing_numbers = [
            int(filename.split('_')[-1].split('.')[0])
            for filename in users_data[user_name]
            if filename.split('_')[-1].split('.')[0].isdigit()
        ]
        if existing_numbers:
            return max(existing_numbers) + 1
    return 1

def register_new_user():
    def capture_photo(actual_name):
        cap = cv2.VideoCapture(1)
        face_detected = False

        while not face_detected:
            ret, frame = cap.read()
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)

            if face_locations:
                face_detected = True
                # Draw a rectangle around the face
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected! Taking photo in 3 seconds...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow('Register', frame)
                cv2.waitKey(1000)

                for i in range(3, 0, -1):
                    ret, frame = cap.read()  # Capture a new frame for countdown
                    top, right, bottom, left = face_locations[0]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f"Taking photo in {i}...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imshow('Register', frame)
                    cv2.waitKey(1000)

                # Capture a clean frame without any annotations
                ret, clean_frame = cap.read()
                photo_number = get_next_photo_number(actual_name)
                save_path = os.path.join(USER_IMAGES_DIR, f"{actual_name.replace(' ', '_').lower()}_{photo_number}.jpg")
                cv2.imwrite(save_path, clean_frame)  # Save the clean frame
                messagebox.showinfo("Success", f"Photo saved as {save_path}")

                # Add or update the user in the database
                if actual_name in users_data:
                    users_data[actual_name].append(f"{actual_name.replace(' ', '_').lower()}_{photo_number}.jpg")
                else:
                    users_data[actual_name] = [f"{actual_name.replace(' ', '_').lower()}_{photo_number}.jpg"]

                with open(USER_JSON_FILE, 'w') as f:
                    json.dump(users_data, f, indent=4)
                break

            cv2.imshow('Register', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        main_window.deiconify()

    main_window.withdraw()

    actual_name = simpledialog.askstring("Input", "Enter the actual name:")
    if actual_name:
        capture_photo(actual_name)

def select_existing_user():
    if not users_data:
        messagebox.showerror("Error", "No users found!")
        return

    user_action = tk.Toplevel(main_window)
    user_action.title("Select Existing User")

    tk.Label(user_action, text="Select User:").pack(pady=10)

    user_var = tk.StringVar(user_action)
    user_var.set("Select a user")  # default value
    dropdown = ttk.Combobox(user_action, textvariable=user_var, values=list(users_data.keys()), state="readonly")
    dropdown.pack(pady=10)

    def on_user_selected():
        selected_user = user_var.get()
        if selected_user and selected_user != "Select a user":
            user_action.destroy()
            user_action_window(selected_user)
        else:
            messagebox.showerror("Error", "Please select a valid user.")

    tk.Button(user_action, text="OK", command=on_user_selected).pack(pady=20)

def user_action_window(user_name):
    def add_more_photos():
        def capture_additional_photo():
            cap = cv2.VideoCapture(1)
            face_detected = False

            while not face_detected:
                ret, frame = cap.read()
                rgb_frame = frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_frame)

                if face_locations:
                    face_detected = True
                    # Draw a rectangle around the face
                    top, right, bottom, left = face_locations[0]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected! Taking photo in 3 seconds...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    cv2.imshow('Add Photo', frame)
                    cv2.waitKey(1000)

                    for i in range(3, 0, -1):
                        ret, frame = cap.read()  # Capture a new frame for countdown
                        top, right, bottom, left = face_locations[0]
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"Taking photo in {i}...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        cv2.imshow('Add Photo', frame)
                        cv2.waitKey(1000)

                    # Capture a clean frame without any annotations
                    ret, clean_frame = cap.read()
                    photo_number = get_next_photo_number(user_name)
                    save_path = os.path.join(USER_IMAGES_DIR, f"{user_name.replace(' ', '_').lower()}_{photo_number}.jpg")
                    cv2.imwrite(save_path, clean_frame)  # Save the clean frame
                    messagebox.showinfo("Success", f"Photo saved as {save_path}")
                    users_data[user_name].append(f"{user_name.replace(' ', '_').lower()}_{photo_number}.jpg")

                    with open(USER_JSON_FILE, 'w') as f:
                        json.dump(users_data, f, indent=4)
                    break

                cv2.imshow('Add Photo', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            user_action.deiconify()

        user_action.withdraw()
        capture_additional_photo()

    def delete_user_account():
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {user_name} and all their photos?"):
            for filename in users_data[user_name]:
                os.remove(os.path.join(USER_IMAGES_DIR, filename))
            del users_data[user_name]
            with open(USER_JSON_FILE, 'w') as f:
                json.dump(users_data, f, indent=4)
            messagebox.showinfo("Deleted", f"User {user_name} and their photos have been deleted.")
            user_action.destroy()
            main_window.deiconify()

    user_action = tk.Toplevel(main_window)
    user_action.title("User Action")
    tk.Label(user_action, text=f"Selected User: {user_name}").pack(pady=10)
    tk.Button(user_action, text="Add More Photos", command=add_more_photos).pack(pady=10)
    tk.Button(user_action, text="Delete Account", command=delete_user_account).pack(pady=10)
    tk.Button(user_action, text="Go Back", command=user_action.destroy).pack(pady=10)

# Main Tkinter Window
main_window = tk.Tk()
main_window.title("Face Recognition System")

tk.Button(main_window, text="Register New User", command=register_new_user).pack(pady=20)
tk.Button(main_window, text="Existing User", command=select_existing_user).pack(pady=20)

main_window.mainloop()
