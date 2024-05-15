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


patterns = {
    "yt": ["https://www.youtube.com/", "https://youtu.be/"],
    "torrent": ["magnet:"],
}


class Clipper(tk.Tk):

    def __init__(self) -> None:
        self.clip = ""
        super().__init__()
        self.resizable(0, 0)
        self.geometry("800x400")
        self["bg"] = "grey"

        self.style = ttk.Style(self)
        self.style.configure("TLabel", background="blue", foreground="grey")

        self.button = tk.Button(command=self.change_button)
        self.button.pack()

        self.clip_message = tk.Label(self, wraplength=750, text=f"Current: {self.clip}")
        self.clip_message.config(width=300)
        self.clip_message.pack(pady=1)
        self.clip_message.after(800, self.update)

        self.ytdl_opts = itertools.cycle(ytdl_opts.keys())
        self.current_ytdl_opts = itertools.cycle(ytdl_opts.keys())

        tk.Button(self, text="Process this clip", command=self.process_clip).pack()
        tk.Button(self, text="Clear current", command=self.clear).pack()
        tk.Button(self, text="Quit", command=self.quit_clipper).pack()

        self.change_button()
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

    def change_button(self):
        self.current_ytdl_opts = next(self.ytdl_opts)
        self.button.config(text=self.current_ytdl_opts)

    def clear(self):
        pyperclip.copy("")
        self.clip = ""

    def process_clip(self):
        if any(p in self.clip for p in patterns["yt"]):
            clipper_services.dl_vids([self.clip], ytdl_opts[self.current_ytdl_opts])

        elif any(p in self.clip for p in patterns["torrent"]):
            clipper_services.add_torrents([self.clip])

        else:
            clipper_services.write_to_file(self.clip)

        print(f"processed {self.clip}")
        self.clear()

    def quit_clipper(self):
        self.destroy()


if __name__ == "__main__":
    Clipper()
