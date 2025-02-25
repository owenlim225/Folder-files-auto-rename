import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Main GUI
class Gui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("500x200")
        self.title("Folder Files Auto Rename")
        self.configure(bg="#3A7FF6")

        self.setup_ui()

    def setup_ui(self):
        self.canvas_widget = tk.Canvas(self, bg="ivory", height=180, width=480, bd=0, highlightthickness=0, relief="ridge")
        self.canvas_widget.place(x=10, y=10)

        self.canvas_widget.create_text(240, 30, text="Remove 'spotidownloader.com -' from song titles", fill="#515486", font=("Arial", 13))

        # Folder Selection
        self.canvas_widget.create_text(50, 80, text="Folder Path:", fill="#515486", font=("Arial-BoldMT", 12), anchor="w")
        self.entry_folder_path = tk.Entry(self.canvas_widget, width=30)
        self.entry_folder_path.place(x=150, y=70)

        self.btn_browse = tk.Button(self, text="Browse", command=self.browse_folder, bg="#3A7FF6", fg="ivory")
        self.btn_browse.place(x=400, y=70)

        # Rename Button
        self.btn_rename = tk.Button(self, text="Rename Files", command=self.rename_files, height=2, width=15, bg="Green", fg="ivory")
        self.btn_rename.place(x=180, y=120)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_folder_path.delete(0, tk.END)
            self.entry_folder_path.insert(0, folder_selected)

    def rename_files(self):
        folder_path = self.entry_folder_path.get()

        if not folder_path:
            messagebox.showerror("Error", "Please select a folder.")
            return

        keyword = "spotidownloader.com -"
        renamed_count = 0

        try:
            for filename in os.listdir(folder_path):
                if keyword in filename:
                    new_filename = filename.replace(keyword, "")
                    os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
                    renamed_count += 1

            messagebox.showinfo("Success", f"Renamed {renamed_count} files successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = Gui()
    app.mainloop()
