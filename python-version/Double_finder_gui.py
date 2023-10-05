import os
import sys
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Button, Menu
from tkinter import ttk
from collections import defaultdict

# Constants
START_OFFSETS = [(145, 1985), (2778, 3800)]
SUPPORTED_EXTENSIONS = (".mp3", ".wma", ".wav")

# Global variables
files_list = None  # Store file information globally
listbox = None     # Store the listbox globally for access in delete_selected_files

def read_binary_slice(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        return binary_data[2:140:9]

def delete_selected_files():
    selected_indices = listbox.curselection()
    for idx in reversed(selected_indices):
        file_path = files_list[idx][0]
        try:
            os.remove(file_path)
            listbox.delete(idx)
            del files_list[idx]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete {file_path}")

def main():
    global files_list
    global listbox

    dir_path = str(sys.argv[1])
    if (dir_path != "") and (os.path.exists(dir_path)):
        print("\n>>" + sys.argv[1])

    len_dirs = sum(len(files) for _, _, files in os.walk(dir_path))
    
    # Create a Tkinter window
    window = tk.Tk()
    window.title("מוצא הכפולים")  # Title in Hebrew
    
    # Set RTL layout
    window.tk_setPalette(background="#EAF2FF")  # Light blue background
    
    # Create a menu in Hebrew
    menu = Menu(window)
    window.config(menu=menu)
    file_menu = Menu(menu)
    menu.add_cascade(label="קובץ", menu=file_menu)
    file_menu.add_command(label="יציאה", command=window.quit)
    
    # Create a title label
    title_label = ttk.Label(window, text="מוצא הכפולים", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)
    
    # Create a listbox and scrollbar for displaying duplicate songs
    listbox = Listbox(window, selectmode=tk.MULTIPLE)
    scrollbar = Scrollbar(window, orient=tk.VERTICAL)
    
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
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
        listbox.insert(tk.END, "אין קבצים כפולים")
    else:
        delete_button = Button(window, text="מחק נבחרים", command=delete_selected_files)
        delete_button.pack()
    
    window.mainloop()
    
if __name__ == '__main__':
    main()
