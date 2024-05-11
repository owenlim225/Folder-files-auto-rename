import os
import tkinter as tk
from tkinter import messagebox

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

        # Artist name entry
        self.canvas_widget.create_text(50, 70, text="Artist name", fill="#515486", font=("Arial-BoldMT", int(13)), anchor="w")
        self.entry_artist_name = tk.Entry(self.canvas_widget, width=30)
        self.entry_artist_name.place(x=150, y=60)

        # Folder URL entry
        self.canvas_widget.create_text(50, 100, text="Folder URL", fill="#515486", font=("Arial-BoldMT", int(13)), anchor="w")
        self.entry_Folder_URL = tk.Entry(self.canvas_widget, width=30)
        self.entry_Folder_URL.place(x=150, y=90)       
              
        # Generate button
        self.btn_generate = tk.Button(self, command=self.function, height=2, width=10, text="Generate", bg="#3A7FF6", fg="ivory")
        self.btn_generate.place(x=400, y=140)
        
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

                
if __name__ == "__main__":
    app = Gui()
    app.mainloop()
