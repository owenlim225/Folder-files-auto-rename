import os
import tkinter as tk
from tkinter import messagebox
from mutagen.easyid3 import EasyID3


# Main gui
class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("500x200")
        self.title("Folder files auto rename")
        self.configure(bg="#3A7FF6")

        self.canvas()
        
    def canvas(self):
        self.canvas_widget = tk.Canvas(self, bg="ivory", height=180, width=480, bd=0, highlightthickness=0, relief="ridge")
        self.canvas_widget.place(x=10, y=10)
        
        self.canvas_widget.create_text(240, 20, text="""Remove "[SPOTIFY-DOWNLOADER.COM]" to artist name""", fill="#515486", font=("New Times Roman", int(13)))
        self.canvas_widget.create_text(240, 40, text="(Album only)", fill="#515486", font=("New Times Roman", int(13)))

        self.canvas_widget.create_text(50, 70, text="Artist name", fill="#515486", font=("Arial-BoldMT", int(13)), anchor="w")
        self.entry_artist_name = tk.Entry(self.canvas_widget, width=30)
        self.entry_artist_name.place(x=150, y=60)
        
        self.canvas_widget.create_text(50, 100, text="Folder URL", fill="#515486", font=("Arial-BoldMT", int(13)), anchor="w")
        self.entry_Folder_URL = tk.Entry(self.canvas_widget, width=30)
        self.entry_Folder_URL.place(x=150, y=90)       
              
        # Generate button
        self.btn_generate = tk.Button(self, command=self.function, height=2, width=10, text="Generate", bg="#3A7FF6", fg="ivory")
        self.btn_generate.place(x=400, y=140)
        
        self.btn_auto_generate = tk.Button(self, command=self.auto_function, height=2, width=10, text="Auto", bg="Green", fg="ivory")
        self.btn_auto_generate.place(x=300, y=140)
        
    def function(self):
        folder_path = self.entry_Folder_URL.get()
        artist_name = self.entry_artist_name.get()
        
        if not folder_path:
            messagebox.showerror(title="Empty Fields!", message="Please enter Folder Path.")
            return
        
        if not artist_name:
            messagebox.showerror(title="Empty Fields!", message="Please enter Artist Name.")
            return

        for filename in os.listdir(folder_path):
            if "[SPOTIFY-DOWNLOADER.COM]" in filename:
                new_filename = filename.replace("[SPOTIFY-DOWNLOADER.COM]", artist_name)
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        
        tk.messagebox.showinfo("Success!", f"Album successfully renamed.")


    def auto_function(self):
        folder_path = self.entry_Folder_URL.get()
        
        if not folder_path:
            messagebox.showerror(title="Empty Fields!", message="Please enter Folder Path.")
            return

        for filename in os.listdir(folder_path):
            if "[SPOTIFY-DOWNLOADER.COM]" in filename:
                file_path = os.path.join(folder_path, filename)
                try:
                    audio = EasyID3(file_path)
                    artist_name = audio['artist'][0]
                except Exception as e:
                    messagebox.showwarning(title="Warning", message=f"Failed to get artist name for {filename}: {str(e)}")
                    continue
                
                # Replace invalid characters with valid ones
                new_artist_name = artist_name.replace("/", "-")
                song_name = filename.split("[SPOTIFY-DOWNLOADER.COM]")[1].strip()
                new_filename = f"{new_artist_name} - {song_name}"
                
                # Rename the file
                try:
                    os.rename(file_path, os.path.join(folder_path, new_filename))
                except Exception as e:
                    messagebox.showwarning(title="Warning", message=f"Failed to rename file {filename}: {str(e)}")
        
        tk.messagebox.showinfo("Success!", f"Albums successfully renamed.")
                
if __name__ == "__main__":
    app = Gui()
    app.mainloop()
