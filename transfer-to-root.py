import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def flatten_folder_structure(root_folder):
    moved = 0
    skipped = 0
    for dirpath, dirnames, filenames in os.walk(root_folder, topdown=False):
        if dirpath == root_folder:
            continue

        for filename in filenames:
            src_path = os.path.join(dirpath, filename)
            dest_path = os.path.join(root_folder, filename)

            if os.path.exists(dest_path):
                skipped += 1
                continue

            shutil.move(src_path, dest_path)
            moved += 1

        if not os.listdir(dirpath):
            os.rmdir(dirpath)

    return moved, skipped

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_folder_path.delete(0, tk.END)
        entry_folder_path.insert(0, folder_selected)

def start_cleanup():
    folder_path = entry_folder_path.get()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    moved, skipped = flatten_folder_structure(folder_path)
    messagebox.showinfo("Done", f"Moved: {moved} files\nSkipped (conflicts): {skipped}")

# Setup UI
root = tk.Tk()
root.title("Folder Flattener")
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
