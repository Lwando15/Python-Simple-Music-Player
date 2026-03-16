import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x400")

        # Variables
        self.playlist = []
        self.current_index = -1

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Playlist display
        self.playlist_box = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="lightgray", fg="black", width=50, height=15)
        self.playlist_box.pack(pady=10)

        # Control buttons
        controls_frame = tk.Frame(self.root)
        controls_frame.pack()

        self.play_btn = tk.Button(controls_frame, text="Play", command=self.play_song_with_vlc, width=10)
        self.play_btn.grid(row=0, column=0, padx=5)

        self.next_btn = tk.Button(controls_frame, text="Next", command=self.next_song, width=10)
        self.next_btn.grid(row=0, column=1, padx=5)

        # Add song button
        self.add_song_btn = tk.Button(self.root, text="Add Song", command=self.add_song, width=20)
        self.add_song_btn.pack(pady=5)

        # Current song label
        self.current_song_label = tk.Label(self.root, text="No song playing", bg="lightgray", width=50)
        self.current_song_label.pack(pady=10)

    def add_song(self):
        # Open file dialog to select song
        files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        if not files:
            return

        for file in files:
            self.playlist.append(file)
            self.playlist_box.insert(tk.END, os.path.basename(file))

    def play_song_with_vlc(self):
        if not self.playlist:
            messagebox.showerror("Error", "Playlist is empty. Please add songs.")
            return

        if self.current_index == -1:
            self.current_index = 0

        try:
            # Get the VLC executable path (adjust as needed)
            vlc_path = "C:/Program Files/VideoLAN/VLC/vlc.exe"  # Replace with your VLC path
            song_path = self.playlist[self.current_index]

            # Construct the VLC command
            vlc_command = f"{vlc_path} \"{song_path}\""

            # Execute the VLC command
            subprocess.run(vlc_command)

            self.update_current_song_label()

        except Exception as e:
            print(f"Error playing song with VLC: {e}")
            messagebox.showerror("Error", f"Could not play song with VLC: {e}")
            self.next_song()  # Skip to the next song on error

    def next_song(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_song_with_vlc()

    def update_current_song_label(self):
        if self.current_index == -1:
            self.current_song_label.config(text="No song playing")
        else:
            current_song = os.path.basename(self.playlist[self.current_index])
            self.current_song_label.config(text=f"Playing: {current_song}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()