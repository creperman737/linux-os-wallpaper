import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIVE_SCRIPT = os.path.join(BASE_DIR, "live.py")
DEFAULT_VIDEO = os.path.join(BASE_DIR, "video.mp4")


class WallpaperPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Wallpaper")
        self.root.geometry("460x220")
        self.root.resizable(False, False)
        self.process = None
        self.video_path = DEFAULT_VIDEO

        tk.Label(root, text="Live Wallpaper", font=("sans", 18, "bold")).pack(pady=(18, 4))
        self.path_label = tk.Label(root, text=self.video_path, anchor="w", width=52)
        self.path_label.pack(padx=18, pady=8)

        buttons = tk.Frame(root)
        buttons.pack(pady=8)
        tk.Button(buttons, text="Videoni tanlash", command=self.choose_video, width=18).grid(row=0, column=0, padx=5)
        tk.Button(buttons, text="Ishga tushirish", command=self.start, width=18).grid(row=0, column=1, padx=5)
        tk.Button(buttons, text="To'xtatish", command=self.stop, width=18).grid(row=1, column=0, columnspan=2, pady=10)

        self.status = tk.Label(root, text="Tayyor", fg="#555")
        self.status.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def choose_video(self):
        selected = filedialog.askopenfilename(
            title="Video tanlang",
            filetypes=[("Video fayllar", "*.mp4 *.mkv *.webm *.avi *.mov"), ("Barcha fayllar", "*.*")],
        )
        if selected:
            self.video_path = selected
            self.path_label.config(text=selected)
            self.status.config(text="Video tanlandi")

    def start(self):
        self.stop(show_status=False)
        if not os.path.exists(self.video_path):
            messagebox.showerror("Xatolik", "Video fayli topilmadi.")
            return
        try:
            self.process = subprocess.Popen([sys.executable, LIVE_SCRIPT, self.video_path])
            self.status.config(text="Wallpaper ishga tushdi")
        except OSError as error:
            messagebox.showerror("Xatolik", str(error))

    def stop(self, show_status=True):
        subprocess.run([os.path.join(BASE_DIR, "stop.sh")], check=False)
        self.process = None
        if show_status:
            self.status.config(text="Wallpaper to'xtatildi")

    def close(self):
        self.stop(show_status=False)
        self.root.destroy()


root = tk.Tk()
WallpaperPanel(root)
root.mainloop()