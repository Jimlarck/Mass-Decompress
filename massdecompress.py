import os
import zipfile
import tkinter as tk
from tkinter import filedialog
import dearpygui.dearpygui as dpg

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
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window
    folder_selected = filedialog.askdirectory()
    root.destroy()
    return folder_selected

def select_folder_callback(sender, app_data, user_data):
    folder = pick_folder()
    if folder:
        dpg.set_value("selected_folder_text", f"Selected Folder: {folder}")
        # Store the folder path as the user data of the Begin Decompression button
        dpg.set_item_user_data("begin_decompression_btn", folder)
    else:
        dpg.set_value("selected_folder_text", "No folder selected.")

def begin_decompression_callback(sender, app_data, user_data):
    folder_path = dpg.get_item_user_data("begin_decompression_btn")
    delete_original = dpg.get_value("delete_checkbox")
    if folder_path:
        print(f"Starting decompression in: {folder_path}")
        decompress_zips(folder_path, delete_original=delete_original)
        dpg.set_value("status_text", f"Decompression complete for folder:\n{folder_path}\nDelete Original: {delete_original}")
    else:
        dpg.set_value("status_text", "Please select a folder first.")

# --- Initialize Dear PyGui Context ---
dpg.create_context()

# Create a single primary window to hold all widgets.
with dpg.window(label="ZIP Decompressor", tag="primary_window", width=500, height=300):
    dpg.add_text("Select a folder to begin decompression:")
    dpg.add_button(label="Select Folder", callback=select_folder_callback)
    dpg.add_text("", tag="selected_folder_text")
    dpg.add_spacing(count=5)
    
    # Checkbox to enable deletion of the original zip files.
    dpg.add_checkbox(label="Delete Original ZIP Files", tag="delete_checkbox", default_value=False)
    dpg.add_spacing(count=5)
    
    dpg.add_button(label="Begin Decompression", tag="begin_decompression_btn", callback=begin_decompression_callback)
    dpg.add_spacing(count=5)
    dpg.add_text("", tag="status_text")

# Mark the window as primary so it becomes the container for our interface.
dpg.set_primary_window("primary_window", True)

# --- Setup and Run the Dear PyGui Viewport ---
dpg.create_viewport(title='ZIP Decompressor', width=800, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
