import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

# File type categories
FILE_TYPE_GROUPS = {
    '.mid': 'MIDI Files',
    '.midi': 'MIDI Files',
    '.wav': 'WAV Files',
    '.mp3': 'MP3 Files',
    '.fst': 'Preset Files',
    '.fxp': 'Preset Files',
}

# Common "noise" words to ignore
NOISE_WORDS = {'mix', 'with', 'ver', 'version', 'v1', 'v2', 'final', 'alt', 'edit'}

user_keywords = []

def normalize_name(filename):
    name = os.path.splitext(filename)[0].lower()
    words = re.findall(r'\w+', name)
    filtered = [w for w in words if not w.isdigit() and w not in NOISE_WORDS]
    return ' '.join(filtered[:3]).strip()

def match_user_keywords(filename, keywords):
    """Return the first keyword that appears in the filename, else None"""
    lower_name = filename.lower()
    for keyword in keywords:
        if keyword.lower() in lower_name:
            return keyword.strip()
    return None

def organize_files_by_smart_keywords(folder_path, keywords):
    if not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path.")

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    groups = defaultdict(list)

    for f in files:
        ext = os.path.splitext(f)[1].lower()
        type_group = FILE_TYPE_GROUPS.get(ext)
        if not type_group:
            continue

        matched_keyword = match_user_keywords(f, keywords)
        group_name = matched_keyword if matched_keyword else normalize_name(f)
        groups[(type_group, group_name)].append(f)

    for (type_group, group_name), group_files in groups.items():
        type_folder = os.path.join(folder_path, type_group)
        os.makedirs(type_folder, exist_ok=True)

        group_folder = os.path.join(type_folder, group_name.title())
        os.makedirs(group_folder, exist_ok=True)

        for f in group_files:
            src = os.path.join(folder_path, f)
            dst = os.path.join(group_folder, f)
            if not os.path.exists(dst):
                shutil.move(src, dst)

    return "Files grouped by smart keywords and user-defined tags!"

# --- GUI STUFF ---

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_folder_path.delete(0, tk.END)
        entry_folder_path.insert(0, folder_selected)

def start_sorting():
    folder_path = entry_folder_path.get()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    raw_keywords = entry_keywords.get()
    keywords = [k.strip() for k in raw_keywords.split(',') if k.strip()]
    try:
        result = organize_files_by_smart_keywords(folder_path, keywords)
        messagebox.showinfo("Done", result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- GUI Layout ---
root = tk.Tk()
root.title("Smart Audio File Organizer")
root.geometry("500x250")
root.resizable(False, False)

canvas = tk.Canvas(root, width=500, height=250, bg="#f0f0f0", highlightthickness=0)
canvas.pack()

canvas.create_text(50, 60, text="Folder Path:", fill="#515486", font=("Arial-BoldMT", 12), anchor="w")
entry_folder_path = tk.Entry(canvas, width=40)
entry_folder_path.place(x=150, y=50)

canvas.create_text(50, 100, text="Keywords (comma-separated):", fill="#515486", font=("Arial-BoldMT", 12), anchor="w")
entry_keywords = tk.Entry(canvas, width=40)
entry_keywords.place(x=250, y=90)

btn_browse = tk.Button(root, text="Browse", command=browse_folder)
btn_browse.place(x=400, y=46)

btn_start = tk.Button(root, text="Start Sorting", bg="#4CAF50", fg="white", command=start_sorting)
btn_start.place(x=200, y=150)

root.mainloop()