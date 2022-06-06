#!/usr/bin/python3

import argparse
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


def get_cl_args():
    parser = argparse.ArgumentParser(description='add these torrents')
    parser.add_argument('links', type=str, nargs='*')
    args = parser.parse_args()
    return args


def start_up():
    cla = get_cl_args()
    vid_list = cla.links
    print("System clipboard to youtube-dl. Press enter when done")
    if new_clip:=check_clipboard():
        resp = input("But first, download current clipboard? (default yes)")
        if not resp.lower().startswith('n'):
            pyperclip.copy(new_clip)
    return vid_list


def main():
    vid_list = start_up()
    stop_list = []
    _thread.start_new_thread(input_thread, (stop_list,))
    while not stop_list:
        if new_clip:=check_clipboard():
            vid_list.append(new_clip)
            print(f'added: {new_clip}')
    ydl_opts = {
        "format": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        'outtmpl': '~/Videos/yt/%(title)s.%(ext)s',
    }
    if vid_list:
        print("Done clipping, start downloading!")
        dl_vids(vid_list, ydl_opts)

if __name__ == "__main__":
    main()
