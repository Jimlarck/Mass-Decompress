import os
import zipfile
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

def decompress_zips(root_dir, delete_original=False):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(root)
                    print(f"Successfully extracted: {zip_path}")
                    
                    # If deletion is enabled, remove the zip file after extraction.
                    if delete_original:
                        os.remove(zip_path)
                        print(f"Removed original ZIP: {zip_path}")
                    
                except zipfile.BadZipFile:
                    print(f"Error: {zip_path} is not a valid ZIP file or is corrupted")
                except Exception as e:
                    print(f"Failed to extract {zip_path}: {str(e)}")

def pick_folder():
    folder_selected = filedialog.askdirectory()
    return folder_selected

def select_folder_callback():
    folder = pick_folder()
    if folder:
        selected_folder_text.set(f"Selected Folder: {folder}")
        # Store the folder path in the user data of the button
        begin_decompression_btn.configure(command=lambda: begin_decompression_callback(folder))

def begin_decompression_callback(folder_path):
    delete_original = delete_checkbox_var.get()
    if folder_path:
        print(f"Starting decompression in: {folder_path}")
        decompress_zips(folder_path, delete_original=delete_original)
        status_text.set(f"Decompression complete for folder:\n{folder_path}\nDelete Original: {delete_original}")
    else:
        status_text.set("Please select a folder first.")

# --- Initialize CustomTkinter UI ---
ctk.set_appearance_mode("System")  # Optional: Set the theme (Light/Dark)
ctk.set_default_color_theme("blue")  # Optional: Set the default theme color

# Scaling factor
scale_factor = 1.5

# Create the main window
root = ctk.CTk()

# Set window title and size
root.title("ZIP Decompressor")
root.geometry(f"{int(500 * scale_factor)}x{int(300 * scale_factor)}")

# Create widgets with scaling applied
select_folder_button = ctk.CTkButton(root, text="Select Folder", command=select_folder_callback, width=int(150 * scale_factor), height=int(40 * scale_factor), font=("Arial", int(14 * scale_factor)))
selected_folder_text = ctk.StringVar(value="")  # Text to display selected folder
selected_folder_label = ctk.CTkLabel(root, textvariable=selected_folder_text, font=("Arial", int(12 * scale_factor)))

delete_checkbox_var = ctk.BooleanVar()
delete_checkbox = ctk.CTkCheckBox(root, text="Delete Original ZIP Files", variable=delete_checkbox_var, font=("Arial", int(12 * scale_factor)))

begin_decompression_btn = ctk.CTkButton(root, text="Begin Decompression", state="disabled", width=int(200 * scale_factor), height=int(40 * scale_factor), font=("Arial", int(14 * scale_factor)))
status_text = ctk.StringVar(value="")
status_label = ctk.CTkLabel(root, textvariable=status_text, font=("Arial", int(12 * scale_factor)))

# Layout the widgets in the window
select_folder_button.pack(pady=int(10 * scale_factor))
selected_folder_label.pack(pady=int(5 * scale_factor))
delete_checkbox.pack(pady=int(5 * scale_factor))
begin_decompression_btn.pack(pady=int(10 * scale_factor))
status_label.pack(pady=int(10 * scale_factor))

# Start the Tkinter main loop
root.mainloop()
