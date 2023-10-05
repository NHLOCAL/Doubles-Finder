import os
import sys
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, Button

# Constants
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
    window.title("Duplicate Songs Deleter")
    
    # Create a listbox and scrollbar for displaying duplicate songs
    listbox = Listbox(window, selectmode=tk.MULTIPLE)
    scrollbar = Scrollbar(window, orient=tk.VERTICAL)
    
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    delete_button = Button(window, text="Delete Selected", command=delete_selected_files)
    delete_button.pack()
    
    files_list = []
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            len_item = len(files_list) + 1
            show_len = len_item * 100 // len_dirs
            print(f"{show_len}% הושלמו", end='\r')
            
            if not file.endswith(SUPPORTED_EXTENSIONS):
                continue
            
            id_file = read_binary_slice(os.path.join(root, file))
            files_list.append((os.path.join(root, file), id_file))
            listbox.insert(tk.END, os.path.join(root, file))
    
    window.mainloop()
    
if __name__ == '__main__':
    main()
