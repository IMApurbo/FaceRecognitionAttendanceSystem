import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk
import cv2
import os
import time
import face_recognition

# Directory to save user images
USER_IMAGES_DIR = 'user_images'

if not os.path.exists(USER_IMAGES_DIR):
    os.makedirs(USER_IMAGES_DIR)

def register_new_user():
    def capture_photo():
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
                photo_name = simpledialog.askstring("Input", "Enter the image saving name:")
                actual_name = simpledialog.askstring("Input", "Enter the actual name:")
                save_path = os.path.join(USER_IMAGES_DIR, photo_name + '.jpg')
                cv2.imwrite(save_path, clean_frame)  # Save the clean frame
                messagebox.showinfo("Success", f"Photo saved as {save_path}")
                add_user_to_database(actual_name, photo_name)
                break

            cv2.imshow('Register', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        main_window.deiconify()

    main_window.withdraw()
    capture_photo()

def add_user_to_database(actual_name, photo_name):
    user_file = os.path.join(USER_IMAGES_DIR, 'users.txt')
    with open(user_file, 'a') as f:
        f.write(f"{actual_name},{photo_name}\n")

def load_users():
    user_file = os.path.join(USER_IMAGES_DIR, 'users.txt')
    users = {}
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                actual_name, photo_name = line.strip().split(',')
                users[actual_name] = photo_name
    return users

def select_existing_user():
    users = load_users()
    if not users:
        messagebox.showerror("Error", "No users found!")
        return

    user_action = tk.Toplevel(main_window)
    user_action.title("Select Existing User")

    tk.Label(user_action, text="Select User:").pack(pady=10)

    user_var = tk.StringVar(user_action)
    user_var.set("Select a user")  # default value
    dropdown = ttk.Combobox(user_action, textvariable=user_var, values=list(users.keys()), state="readonly")
    dropdown.pack(pady=10)

    def on_user_selected():
        selected_user = user_var.get()
        if selected_user and selected_user != "Select a user":
            user_action.destroy()
            user_action_window(selected_user, users[selected_user])
        else:
            messagebox.showerror("Error", "Please select a valid user.")

    tk.Button(user_action, text="OK", command=on_user_selected).pack(pady=20)

def user_action_window(user_name, photo_name):
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
                    save_path = os.path.join(USER_IMAGES_DIR, f"{photo_name}_{time.time()}.jpg")
                    cv2.imwrite(save_path, clean_frame)  # Save the clean frame
                    messagebox.showinfo("Success", f"Photo saved as {save_path}")
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
        user_file = os.path.join(USER_IMAGES_DIR, 'users.txt')
        with open(user_file, 'r') as f:
            lines = f.readlines()
        with open(user_file, 'w') as f:
            for line in lines:
                if line.strip().split(',')[0] != user_name:
                    f.write(line)
        
        for filename in os.listdir(USER_IMAGES_DIR):
            if filename.startswith(photo_name):
                os.remove(os.path.join(USER_IMAGES_DIR, filename))

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
