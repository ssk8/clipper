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
        "outtmpl": "~/Videos/yt/%(title)s.%(ext)s",
    },
    "Higher quality (1080p)": {
        "format": "bestvideo[height=1080]+bestaudio/best",
        "subtitleslangs": ["en"],
        "writesubtitles": True,
        "outtmpl": "~/Videos/yt/%(title)s.%(ext)s",
    },
    "Audio only": {
        "format": "m4a/bestaudio/best",
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
        self.clip: str = "empty clipboard"
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
        if new_clip := pyperclip.paste():
            self.clip = new_clip
            self.clip_message.configure(text=f"Current: {self.clip}")
        else:
            self.clip_message.configure(text=f"Current: clipboard empty")
        self.clip_message.after(800, self.update)

    def change_button(self):
        self.current_ytdl_opts = next(self.ytdl_opts)
        self.button.config(text=self.current_ytdl_opts)

    def clear(self):
        pyperclip.copy('')
        self.clip = ""
        

    def process_clip(self):
        if any(p in self.clip for p in patterns["yt"]):
            clipper_services.dl_vids([self.clip], ytdl_opts[self.current_ytdl_opts])

        if any(p in self.clip for p in patterns["torrent"]):
            clipper_services.add_torrents([self.clip])

        print(f"processed {self.clip}")
        pyperclip.copy('')

    def quit_clipper(self):
        self.process_clip()
        self.destroy()


if __name__ == "__main__":
    Clipper()
