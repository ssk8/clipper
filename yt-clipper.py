#!/usr/bin/python3

import youtube_dl
import pyperclip
import _thread


def input_thread(stop_list):
    input()
    stop_list.append(True)


def dl_vids(vid_list, ydl_opts = {}):
    for vid in vid_list: print(vid)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(vid_list)


def check_clipboard():
    if new_clip:=pyperclip.paste():
        pyperclip.copy('')
        return new_clip


def start_up():
    print("System clipboard to youtube-dl. Press enter when done")
    if new_clip:=check_clipboard():
        resp = input("But first, download current clipboard? (default yes)")
        if not resp.lower().startswith('n'):
            pyperclip.copy(new_clip)


def main():
    start_up()
    vid_list = []
    stop_list = []
    _thread.start_new_thread(input_thread, (stop_list,))
    while not stop_list:
        if new_clip:=check_clipboard():
            vid_list.append(new_clip)
            print(f'added: {new_clip}')
    ydl_opts = {
        "format": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        'outtmpl': '/home/curt/Videos/yt/%(title)s.%(ext)s',
    }
    if vid_list:
        print("Done clipping, start downloading!")
        dl_vids(vid_list, ydl_opts)

if __name__ == "__main__":
    main()