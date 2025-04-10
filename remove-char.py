import os
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_dot_underscore_files(folder_path):
    deleted_files = []
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.startswith("._"):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
    return deleted_files

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_folder_path.delete(0, tk.END)
        entry_folder_path.insert(0, folder_selected)

def start_cleanup():
    folder_path = entry_folder_path.get()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid folder path.")
        return

    deleted_files = remove_dot_underscore_files(folder_path)
    message = f"Deleted {len(deleted_files)} file(s) starting with '._'."
    messagebox.showinfo("Cleanup Complete", message)

# Setup UI
root = tk.Tk()
root.title("._ File Remover")
root.geometry("500x200")
root.resizable(False, False)

canvas = tk.Canvas(root, width=500, height=200, bg="#f0f0f0", highlightthickness=0)
canvas.pack()

# Folder Selection
canvas.create_text(50, 80, text="Folder Path:", fill="#515486", font=("Arial-BoldMT", 12), anchor="w")
entry_folder_path = tk.Entry(canvas, width=40)
entry_folder_path.place(x=150, y=70)

btn_browse = tk.Button(root, text="Browse", command=browse_folder)
btn_browse.place(x=400, y=66)

# Start Button
btn_start = tk.Button(root, text="Start Cleanup", bg="#4CAF50", fg="white", command=start_cleanup)
btn_start.place(x=200, y=120)

root.mainloop()
