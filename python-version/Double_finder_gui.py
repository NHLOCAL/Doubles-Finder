import os
import sys
import tkinter as tk
from tkinter import messagebox, Listbox, Button, Menu, Entry, filedialog, ttk
from collections import defaultdict
import threading
import time

# Constants
SUPPORTED_EXTENSIONS = (".mp3", ".wma", ".wav")

# Global variables
files_list = None  # Store file information globally
listbox = None     # Store the listbox globally for access in delete_selected_files
folder_entry = None  # Store the folder path entry globally
progress_bar = None  # Store the progress bar globally
scan_button = None  # Store the Scan button globally

def read_binary_slice(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return binary_data

def delete_selected_files():
    selected_indices = listbox.curselection()
    for idx in reversed(selected_indices):
        # Check if the selected item is not "No duplicate files" before deleting
        if listbox.get(idx) != "No duplicate files":
            file_path = files_list[idx][0]
            try:
                os.remove(file_path)
                listbox.delete(idx)
                del files_list[idx]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete {file_path}")

def scan_folder():
    global files_list
    global listbox

    dir_path = folder_entry.get()
    if (dir_path != "") and (os.path.exists(dir_path)):
        len_dirs = sum(len(files) for _, _, files in os.walk(dir_path))

        files_list = []
        file_dict = defaultdict(list)

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if not file.endswith(SUPPORTED_EXTENSIONS):
                    continue

                id_file = read_binary_slice(os.path.join(root, file))
                files_list.append((os.path.join(root, file), id_file))
                file_dict[id_file].append(os.path.join(root, file))

        duplicate_files_found = False

        for id_item, file_paths in file_dict.items():
            if len(file_paths) > 1:
                duplicate_files_found = True
                for file_path in file_paths:
                    listbox.insert(tk.END, file_path)

        if not duplicate_files_found:
            listbox.insert(tk.END, "לא נמצאו קבצים כפולים")

def scan_and_update_progress():
    global listbox

    # Clear the listbox
    listbox.delete(0, tk.END)

    # Disable the Scan button during scanning
    scan_button.config(state=tk.DISABLED)
    folder_path = folder_entry.get()

    def update_progress():
        progress = 0
        for _ in os.walk(folder_path):
            progress += 1
        return progress

    total_dirs = update_progress()
    if total_dirs == 0:
        total_dirs = 1  # Prevent division by zero

    progress_step = 100 / total_dirs
    progress_value = 0

    for _ in os.walk(folder_path):
        progress_value += progress_step
        progress_bar["value"] = progress_value
        progress_bar.update()
        time.sleep(0.1)  # Introduce a delay to slow down the progress bar
    progress_bar["value"] = 100

    # Re-enable the Scan button after scanning
    scan_button.config(state=tk.NORMAL)
    scan_folder()  # Update the listbox after scanning

def browse_folder():
    global folder_entry
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, selected_folder)

def main():
    global files_list
    global listbox
    global folder_entry
    global progress_bar
    global scan_button

    # Create a Tkinter window
    window = tk.Tk()
    window.title("מוצא הכפולים")  # Title in English

    # Set the window's size
    window.geometry("500x600")

    # Create a menu in English
    menu = Menu(window)
    window.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label="קובץ", menu=file_menu)
    file_menu.add_command(label="יציאה", command=window.quit)

    # Create an Entry for folder path
    folder_entry = Entry(window, width=50, font=("Tahoma", 12))
    folder_entry.pack(pady=10, padx=20, side=tk.TOP)

    # Create a "Browse" button and position it on the top
    browse_button = Button(window, text="עיין", command=browse_folder, font=("Tahoma", 12))
    browse_button.pack(pady=10, padx=20, side=tk.TOP)

    # Create a "Scan" button
    scan_button = Button(window, text="סרוק", command=lambda: threading.Thread(target=scan_and_update_progress).start(), font=("Tahoma", 14))
    scan_button.pack(pady=20)

    # Create a frame for listbox and scrollbar
    frame = tk.Frame(window)
    frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Create a listbox and scrollbar for displaying duplicate songs
    listbox = Listbox(frame, selectmode=tk.MULTIPLE, font=("Tahoma", 12))
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)

    listbox.config(yscrollcommand=scrollbar.set)
    
    listbox.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    files_list = []

    # Create a "Delete" button (initially hidden)
    delete_button = Button(window, text="מחק נבחרים", command=delete_selected_files, font=("Tahoma", 12))
    delete_button.pack(pady=10)

    def toggle_delete_button(event):
        if listbox.curselection():
            delete_button.pack(pady=10)
        else:
            delete_button.pack_forget()

    listbox.bind('<<ListboxSelect>>', toggle_delete_button)

    # Create a progress bar
    progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=400, mode="determinate")
    progress_bar.pack(pady=10)

    window.mainloop()

if __name__ == '__main__':
    main()
