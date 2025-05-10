import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import pyttsx3
import pygame
import tempfile
import threading
import os

class TTSOfflinePlayer:
    def __init__(self):
        pygame.mixer.init()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.audio_file = None
        self.is_paused = False
        self.is_playing = False

    def generate_audio(self, text):
        self.stop()
        fd, path = tempfile.mkstemp(suffix=".wav", prefix="tts_")
        os.close(fd)
        self.audio_file = path
        self.engine.save_to_file(text, path)
        self.engine.runAndWait()

    def play(self, text, callback):
        self.generate_audio(text)
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()
        self.is_paused = False
        self.is_playing = True
        callback("Pause")

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False

    def resume(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        if self.audio_file and os.path.exists(self.audio_file):
            os.remove(self.audio_file)
        self.audio_file = None
        self.is_paused = False
        self.is_playing = False

    def download_audio(self, text, destination_path):
        self.engine.save_to_file(text, destination_path)
        self.engine.runAndWait()


class TTSOfflineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Text-to-Speech")

        self.tts = TTSOfflinePlayer()

        self.text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
        self.text_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.toggle_btn = ttk.Button(root, text="Play", command=self.toggle_play_pause)
        self.toggle_btn.grid(row=1, column=0, padx=10, pady=10)

        self.download_btn = ttk.Button(root, text="Download", command=self.download_audio_file)
        self.download_btn.grid(row=1, column=1, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.play_thread = None

    def set_button_label(self, label):
        self.toggle_btn.config(text=label)

    def toggle_play_pause(self):
        if not self.tts.is_playing and not self.tts.is_paused:
            text = self.text_box.get("1.0", tk.END).strip()
            if not text:
                return
            self.set_button_label("Loading...")
            self.play_thread = threading.Thread(target=self.tts.play, args=(text, self.set_button_label), daemon=True)
            self.play_thread.start()
        elif self.tts.is_playing:
            self.tts.pause()
            self.set_button_label("Resume")
        elif self.tts.is_paused:
            self.tts.resume()
            self.set_button_label("Pause")

    def download_audio_file(self):
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if file_path:
            threading.Thread(target=self.tts.download_audio, args=(text, file_path), daemon=True).start()

    def on_close(self):
        self.tts.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TTSOfflineApp(root)
    root.mainloop()
