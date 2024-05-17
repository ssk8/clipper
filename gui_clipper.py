#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
import pyperclip
import itertools
import clipper_services

ytdl_opts = {
    "Standard (720p)": {
        "format": "bestvideo[height=720]+bestaudio/best",
        "subtitleslangs": ["en"],
        "writesubtitles": True,
        "outtmpl": "~/Videos/yt/%(title)s.%(id)s.%(ext)s",
    },
    "Higher quality (1080p)": {
        "format": "bestvideo[height=1080]+bestaudio/best",
        "subtitleslangs": ["en"],
        "writesubtitles": True,
        "outtmpl": "~/Videos/yt/%(title)s.%(id)s.%(ext)s",
    },
    "Audio only": {
        "format": "m4a/bestaudio/best",
        "outtmpl": "~/Music/yt/%(title)s.%(id)s.%(ext)s",
    },
    "Audio only → mp3": {
        "format": "m4a/bestaudio/best",
        "outtmpl": "~/Music/yt/%(title)s.%(id)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    },
}


torrent_destinations = {"Downloads":"/home/curt/Downloads/", "other":"/home/curt/other/"}


patterns = {
    "yt": {"https://www.youtube.com/", "https://youtu.be/"},
    "torrent": ["magnet:"],
}


class Clipper(tk.Tk):

    def __init__(self) -> None:
        self.clip = ""
        self.yt_clips = {key:[] for key in ytdl_opts.keys()}
        self.torrent_clips = {key:[] for key in torrent_destinations.keys()}
        super().__init__()
        self.resizable(0, 0)
        self.geometry("800x400")
        self["bg"] = "grey"

        self.style = ttk.Style(self)
        self.style.configure("TLabel", background="blue", foreground="grey")

        self.yt_button = tk.Button(command=self.change_yt_button)
        self.yt_button.pack(ipadx=20, anchor=tk.N, side=tk.TOP, expand=True)

        self.tor_path_button = tk.Button(command=self.change_tp_button)
        self.tor_path_button.pack(ipadx=20, anchor=tk.N, side=tk.TOP, expand=True)

        self.clip_message = tk.Label(self, wraplength=750, text=f"Current: {self.clip}")
        self.clip_message.config(width=110, height=15)
        self.clip_message.pack(pady=1)
        self.clip_message.after(800, self.update)

        self.ytdl_opts = itertools.cycle(ytdl_opts.keys())
        self.current_ytdl_opts = self.ytdl_opts
        
        self.tor_paths = itertools.cycle(torrent_destinations.keys())
        self.current_tor_paths = self.tor_paths

        tk.Button(self, text="Process clips", command=self.process_clips).pack(ipadx=20, anchor=tk.S, side=tk.LEFT, expand=True)
        tk.Button(self, text="Clear current", command=self.clear).pack(ipadx=20, ipady=2, anchor=tk.S, side=tk.LEFT, expand=True)
        tk.Button(self, text="Quit", command=self.quit_clipper).pack(ipadx=20, ipady=2, anchor=tk.S, side=tk.LEFT, expand=True)

        self.change_yt_button()
        self.change_tp_button()
        self.mainloop()

    def update(self):
        new_clip = pyperclip.paste()
        if not new_clip:
            text = f"clipboard empty"
        elif new_clip != self.clip:
            if self.clip:
                self.process_clip()
            self.clip = new_clip
            text = f"Current: {self.clip}"
        else:
            text = f"Current: {self.clip}"
        self.clip_message.configure(text=text)
        self.clip_message.after(800, self.update)

    def change_yt_button(self):
        self.current_ytdl_opts = next(self.ytdl_opts)
        self.yt_button.config(text=self.current_ytdl_opts)
    
    def change_tp_button(self):
        self.current_tor_paths = next(self.tor_paths)
        self.tor_path_button.config(text=self.current_tor_paths)

    def clear(self):
        pyperclip.copy("")
        self.clip = ""

    def process_clip(self):
        if any(p in self.clip for p in patterns["yt"]):
            self.yt_clips[self.current_ytdl_opts].append(self.clip)

        elif any(p in self.clip for p in patterns["torrent"]):
            self.torrent_clips.append((self.clip, "/home/curt/Downloads/"))

        else:
            clipper_services.write_to_file(self.clip)

        print(f"processed {self.clip}")
        self.clear()

    def process_clips(self):
        self.process_clip()
        for opts, addresses in self.yt_clips.items():
            clipper_services.dl_vids(addresses, opts)

        for path, magnets in self.torrent_clips.items():
            clipper_services.add_torrents(magnets, path)

        print(f"processed clips")
        self.yt_clips = {key:[] for key in ytdl_opts.keys()}
        self.torrent_clips = {key:[] for key in torrent_destinations.keys()}
        

    def quit_clipper(self):
        self.destroy()


if __name__ == "__main__":
    Clipper()
