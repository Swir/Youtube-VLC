import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
from yt_dlp import YoutubeDL
import subprocess
import tempfile
import os

class VideoDownloader:
    def __init__(self):
        self.vlc_path = None

    def open_in_vlc(self, url):
        try:
            if "youtube.com" in url:
                url = self._get_youtube_stream_url(url)
            self._open_in_vlc(url)
        except Exception as e:
            messagebox.showerror("Błąd", f"Niespodziewany błąd:\n{e}")

    def _get_youtube_stream_url(self, url):
        ydl_opts = {
            'format': 'best',
            'extract_flat': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            return result['url']

    def _open_in_vlc(self, url):
        try:
            if self.vlc_path:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                    temp_file.write(url.encode("utf-8"))

                subprocess.run([self.vlc_path, "--playlist-enqueue", temp_file.name], check=True)
                os.unlink(temp_file.name)
            else:
                messagebox.showwarning("Błąd", "Proszę wybrać ścieżkę do VLC Player.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Błąd", f"Błąd podczas otwierania wideo w VLC:\n{e}")

    def set_vlc_path(self, path):
        self.vlc_path = path

class ProgramGUI:
    def __init__(self, master):
        self.master = master
        master.title("Youtube Vlc player by Swir")
        master.configure(bg="#f0f0f0")  # Ustawienie koloru tła
        master.geometry("500x250")  # Ustawienie rozmiaru okna

        self.label_url = tk.Label(master, text="Podaj link do filmu na YouTube:", font=("Helvetica", 12), bg="#f0f0f0")
        self.entry_url = tk.Entry(master, width=40, font=("Helvetica", 10))

        self.button_otworz_vlc = tk.Button(master, text="Otwórz w VLC", command=self.otworz_w_vlc,
                                           font=("Helvetica", 12), bg="#2196F3", fg="white")  # Przycisk o kolorze niebieskim

        self.label_choose_vlc = tk.Label(master, text="Wybierz ścieżkę do VLC:", font=("Helvetica", 12), bg="#f0f0f0")

        self.vlc_options = [
            "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
            "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe",
            "Inna lokalizacja"
        ]

        self.vlc_path_var = tk.StringVar()
        self.vlc_path_var.set(self.vlc_options[0])

        self.dropdown_vlc = ttk.Combobox(master, textvariable=self.vlc_path_var, values=self.vlc_options, state="readonly")
        self.dropdown_vlc.bind("<<ComboboxSelected>>", self.on_dropdown_change)

        self.button_wybierz_vlc = tk.Button(master, text="Wybierz VLC", command=self.wybierz_vlc,
                                           font=("Helvetica", 12), bg="#ff9800", fg="white")  # Przycisk o kolorze pomarańczowym

        self.label_url.pack(pady=(20, 0), padx=10)
        self.entry_url.pack(pady=10, padx=10)
        self.button_otworz_vlc.pack(pady=10)
        self.label_choose_vlc.pack(pady=(20, 0), padx=10)
        self.dropdown_vlc.pack(pady=5)
        self.button_wybierz_vlc.pack(pady=10)

        self.video_downloader = VideoDownloader()

    def otworz_w_vlc(self):
        url = self.entry_url.get()

        if not url:
            messagebox.showwarning("Błąd", "Proszę podać link do filmu na YouTube.")
            return

        self.master.update_idletasks()  # Zaktualizuj widżety, aby natychmiast zobaczyć zmiany

        self.video_downloader.open_in_vlc(url)

    def on_dropdown_change(self, event):
        selected_option = self.vlc_path_var.get()
        if selected_option == "Inna lokalizacja":
            path = filedialog.askopenfilename(filetypes=[("VLC Executable", "*.exe")])
            self.vlc_path_var.set(path)

    def wybierz_vlc(self):
        selected_option = self.vlc_path_var.get()
        if selected_option != "Inna lokalizacja":
            self.video_downloader.set_vlc_path(selected_option)
        else:
            path = filedialog.askopenfilename(filetypes=[("VLC Executable", "*.exe")])
            self.vlc_path_var.set(path)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ProgramGUI(root)
    root.mainloop()
